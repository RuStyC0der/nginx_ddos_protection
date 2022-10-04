from time import time, sleep
from iptables import IptablesBlockMethod
from reader import ChunkReader
from parser import SplitParser

logfile = "nginx_test_conf/log/access.log"


# banner = IptablesBlockMethod()
reader = ChunkReader(logfile)
parser = SplitParser(reader)

frequency_datastore = {}

period_seconds = 0.01
ratelimit = 10
sleep_seconds = 0.5


def filter_ips(frequency_datastore, treshold):
    for ip in frequency_datastore:
        if frequency_datastore[ip] > treshold:
            print(f"ban {ip}")

time_previous = 0
time_delta = 0
for sample in parser:

    # print(sample)
    # sleep(0.1)

    if time_delta > period_seconds:
        filter_ips(frequency_datastore, ratelimit)
        frequency_datastore = {}
        time_delta = 0

    if not sample:
        sleep(sleep_seconds)
        time_delta += sleep_seconds * 1000
        continue

    ip = sample[0]
    timestamp = float(sample[1])

    time_delta += timestamp - time_previous
    time_previous = timestamp

    try:
        frequency_datastore[ip] += 1 
    except KeyError:
        frequency_datastore[ip] = 1