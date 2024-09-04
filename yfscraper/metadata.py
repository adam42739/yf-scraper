import json
import os
import datetime


def get_metadata(base):
    path = base + "_metadata.json"
    data = {}
    if os.path.exists(path):
        with open(path, "r") as file:
            data = json.load(file)
    for ticker in data:
        data[ticker] = datetime.datetime.strptime(data[ticker], "%Y%m%d")
    return data


def write_metadata(data, base):
    for ticker in data:
        data[ticker] = datetime.datetime.strftime(data[ticker], "%Y%m%d")
    path = base + "_metadata.json"
    with open(path, "w") as file:
        json.dump(data, file)
