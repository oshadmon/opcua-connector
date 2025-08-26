import argparse
import datetime
import os
import pandas as pd
import json
import time
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
    'TC1001': 28,
    'TC1002': 29,
    'TC1003': 30,
    'TC1004': 31,
    'TC1005': 32,
    'TC1006': 33,
    'TC1007': 34,
    'TC1008': 35,
    'TC1009': 36,
    'TC1010': 37,
    'TC1011': 38,
    'TC1012': 39
}
}


# Function to POST data
def publish_msg_client(conn:str):
    command = '''
    run msg client where broker=rest and user-agent=anylog and log=false and topic=(
        name=nov and
        dbms="bring [dbms]" and
        table="bring [table]" and
        column.timestamp=(type=timestamp and value="bring [timestamp]") and
        column.value=(type=float and value="bring [value]" and optional=false)
    )>
    '''.replace('\n',' ').replace('\t', ' ')
    headers = {
        'command': command,
        'User-Agent': 'AnyLog/1.23'
    }

    try:
        response = requests.post(url=f'http://{conn}', headers=headers)
        response.raise_for_status()
    except Exception as error:
        raise Exception(f"Failed to execute `run msg client` (Error: {error})")


def post_data(conn: str, payload: list):
    headers = {
        "command": "data",
        "topic": "nov",
        "User-Agent": "AnyLog/1.23",
        "Content-Type": "application/json"
    }

    # for node in payload:
    #     if node['table'] == 't46':
    #         print(f'{node["dbms"]}.{node["table"]} - {node["timestamp"]} | {node["value"]}')

    try:
        response = requests.post(url=f"http://{conn}", headers=headers, data=json.dumps(payload), timeout=60)
        response.raise_for_status()
    except Exception as error:
        print(conn)
        print(payload)
        print(headers)
        raise Exception(f"POST failed: {error}")


def update_timestamp(file_content: list):
    if not file_content:
        return file_content

    # Parse all original timestamps into datetime objects
    original_ts = [
        datetime.datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)
        for row in file_content
    ]

    # Start new series 1 minute after the last timestamp
    min_ts = min(original_ts)
    max_ts = max(original_ts)

    max_curr_timestamp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=(max_ts - min_ts).total_seconds())

    for i in range(len(original_ts)):
        new_ts = max_curr_timestamp - datetime.timedelta(seconds=(max_ts - original_ts[i]).total_seconds())
        file_content[i]['timestamp'] = new_ts.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # # Rebuild timestamps using original increments
    # new_ts = [base_start_ts]
    # for i in range(1, len(original_ts)):
    #     diff = original_ts[i] - original_ts[i - 1]
    #     new_ts.append(new_ts[-1] + diff)
    #
    # # Assign back into file_content
    # for i in range(len(file_content)):
    #

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


def publish_data(conn:str, db_name:str, metadata: str, file_content: list):
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
                    payload['dbms'] = db_name
                    payload['table'] = f't{METADATAS[metadata][column] + 1}'
                    payloads.append(payload)
        if payloads:
            post_data(conn=conn, payload=payloads)


def worker(conn:str, db_name:str, metadata:str, iteration:int):
    print(f"[Thread] {metadata} iteration {iteration}")
    file_content = csv2json(file_path=METADATAS[metadata]['file'])
    # if iteration > 0:
    file_content = update_timestamp(file_content)
    # print(file_content[0]['timestamp'])
    publish_data(conn=conn, db_name=db_name, metadata=metadata, file_content=file_content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('conn', type=str, default=None, help='REST connection to send data against')
    parser.add_argument('--db-name', type=str, default="opcua_demo", help='logical database to store data in')
    parser.add_argument('--create-msg-client', type=bool, nargs='?', const=True, default=False, help='run `get msg client` via REST')
    args = parser.parse_args()

    if args.create_msg_client is True:
        publish_msg_client(conn=args.conn)

    iteration = 0
    while True:
        print(f"=== Iteration {iteration} ===")
        with ThreadPoolExecutor(max_workers=len(METADATAS)) as executor:
            futures = [executor.submit(worker, conn=args.conn, db_name=args.db_name, metadata, iteration) for metadata in METADATAS]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Error in worker: {e}")
        iteration += 1
        time.sleep(30)


if __name__ == '__main__':
    main()