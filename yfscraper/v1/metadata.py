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
        data[ticker]["start_date"] = datetime.datetime.strptime(
            data[ticker]["start_date"], "%Y%m%d"
        )
        data[ticker]["end_date"] = datetime.datetime.strptime(
            data[ticker]["end_date"], "%Y%m%d"
        )
    return data


def write_metadata(data, base):
    data_write = {}
    for ticker in data:
        data_write[ticker] = {
            "start_date": datetime.datetime.strftime(
                data[ticker]["start_date"], "%Y%m%d"
            ),
            "end_date": datetime.datetime.strftime(data[ticker]["end_date"], "%Y%m%d"),
        }
    path = base + "_metadata.json"
    with open(path, "w") as file:
        json.dump(data_write, file)
