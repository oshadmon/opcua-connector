import datetime
import json
import os

def get_data(dir_name):
    full_data = []
    full_dir = os.path.join('data', dir_name)
    if os.path.isdir(full_dir):
        for fname in os.listdir(full_dir):
            full_path = os.path.join(full_dir, fname)

            with open(full_path, 'r') as f:
                for line in f.read().split("\n"):
                    full_data.append(json.loads(line))
    return full_data


def shift_timestamps(data, new_start):
    # Parse the old_start (string -> datetime)
    old_start = datetime.datetime.fromisoformat(data[0]["timestamp"])
    # Compute time delta
    shift = new_start - old_start

    updated = []
    for item in data:
        ts = datetime.datetime.fromisoformat(item["timestamp"])  # parse
        new_ts = ts + shift
        updated.append({
            **item,
            "timestamp": new_ts.isoformat()  # back to string
        })
    return updated
