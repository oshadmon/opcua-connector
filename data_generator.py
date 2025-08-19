import datetime
import os
import pandas as pd
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


# Metadata mapping
METADATAS = {
    "oil system": {
        "file": os.path.join('base_examples', 'hpu_mud_system_oil_data.v6.csv'),
        "oil_flowrate_lpm": 20,
        "oil_temp_supply_c": 45,
        "oil_pressure_kpa": 27,
        "oil_temp_cooled_c": 42
    },
    "main loop": {
        "file": os.path.join('base_examples', 'hpu_mud_system_main_loop_data.v6.csv'),
        "main_loop_flowrate_lpm": 19,
        "discharge_pressure_1_kpa": 24,
        "discharge_pressure_2_kpa": 25
    },
    "thermocouples": {
        "file": os.path.join('base_examples', 'hpu_mud_system_thermocouple_data.v6.csv'),
        'TC1001': 31,
        'TC1002': 32,
        'TC1003': 33,
        'TC1004': 34,
        'TC1005': 35,
        'TC1006': 36,
        'TC1007': 37,
        'TC1008': 38,
        'TC1009': 39,
        'TC1010': 40,
        'TC1011': 41,
        'TC1012': 42
    }
}


# Function to POST data
def post_data(conn: str, payload: list):
    headers = {
        "command": "data",
        "topic": "nov",
        "User-Agent": "AnyLog/1.23",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url=f"http://{conn}", headers=headers, data=json.dumps(payload), timeout=60)
        response.raise_for_status()
    except Exception as error:
        raise Exception(f"POST failed: {error}")


def update_timestamp(file_content: list):
    if not file_content:
        return file_content

    # Parse all original timestamps into datetime objects
    original_ts = [
        datetime.datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        for row in file_content
    ]

    # Start new series 1 minute after the last timestamp
    base_start_ts = original_ts[-1] + datetime.timedelta(minutes=1)

    # Rebuild timestamps using original increments
    new_ts = [base_start_ts]
    for i in range(1, len(original_ts)):
        diff = original_ts[i] - original_ts[i - 1]
        new_ts.append(new_ts[-1] + diff)

    # Assign back into file_content
    for i in range(len(file_content)):
        file_content[i]['timestamp'] = new_ts[i].strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return file_content

def csv2json(file_path: str):
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        return json.loads(df.to_json(orient="records", lines=False))


def update_timestamp_orig(file_content: list):
    min_ts = None
    max_ts = None

    for i in range(len(file_content)):
        ts = datetime.datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
    for row in file_content:
        ts = datetime.datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')
        if not min_ts:
            min_ts = ts
        if not max_ts or max_ts < ts:
            max_ts = ts

    time_diff = max_ts - min_ts
    base_start_ts = max_ts + datetime.timedelta(minutes=1)
    increments = (time_diff.total_seconds() / max(1, len(file_content) - 1))

    # Assign new timestamps in order
    for i in range(len(file_content)):
        file_content[i]['timestamp'] = (base_start_ts + datetime.timedelta(seconds=(increments * i))).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return file_content


def publish_data(metadata: str, file_content: list):
    for row in file_content:
        payloads = []
        for column, value in row.items():
            # if file_content.index(row) == 0 or row == file_content[-1]:
            #     print(column, value, row['timestamp'])
            if column not in ['timestamp', 'file']:
                payload = {
                    'timestamp': row['timestamp'],
                    'table': None,
                    'value': value
                }
                if column in METADATAS[metadata]:
                    payload['dbms'] = 'nov'
                    payload['table'] = f't{METADATAS[metadata][column] + 1}'
                    payloads.append(payload)
        if payloads:
            post_data(conn='10.0.0.39:32249', payload=payloads)


def worker(metadata: str, iteration: int):
    print(f"[Thread] {metadata} iteration {iteration}")
    file_content = csv2json(file_path=METADATAS[metadata]['file'])
    if iteration > 0:
        file_content = update_timestamp(file_content)
    # print(file_content[0]['timestamp'])
    publish_data(metadata=metadata, file_content=file_content)


def main():
    iteration = 0
    while True:
        print(f"=== Iteration {iteration} ===")
        with ThreadPoolExecutor(max_workers=len(METADATAS)) as executor:
            futures = [executor.submit(worker, metadata, iteration) for metadata in METADATAS]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in worker: {e}")
        iteration += 1


if __name__ == '__main__':
    main()