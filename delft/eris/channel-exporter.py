#!/usr/bin/env python3

import requests
from dateutil.parser import parse
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import sys
from pprint import pprint
import json

CHANNEL_REQUEST_TIME = Histogram(
    "channel_request_time", "Time spent requesting channel data"
)
CHANNEL_UPDATE_TIME = Gauge(
    "channel_update_time",
    "Total number of failures to fetch spot market prices",
    ["channel"],
)
CHANNEL_CURRENT = Gauge(
    "channel_current",
    "If a channel is expected to be current",
    ["channel"],
)
CHANNEL_REQUEST_FAILURES = Counter(
    "channel_request_failures_total",
    "Number of channel status requests which have failed",
)


@CHANNEL_REQUEST_TIME.time()
def measure_channel(name):
    try:
        with CHANNEL_REQUEST_FAILURES.count_exceptions():
            result = requests.get(f"https://nixos.org/channels/{name}")
        return parse(result.headers["last-modified"]).timestamp()
    except Exception as e:
        pprint(e)


if __name__ == "__main__":
    start_http_server(9402)

    with open(sys.argv[1]) as channel_data:
        channels = json.load(channel_data)

    while True:
        for (channel, about) in channels.items():
            measurement = measure_channel(channel)
            if measurement is not None:
                CHANNEL_UPDATE_TIME.labels(channel=channel).set(measurement)
                CHANNEL_CURRENT.labels(channel=channel).set(int(about['current']))
        time.sleep(60)