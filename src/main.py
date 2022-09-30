from time import time, sleep
from iptables import IptablesBlockMethod
from reader import ChunkReader
from parser import SplitParser

logfile = "nginx_test_conf/log/access.log"


# banner = IptablesBlockMethod()
reader = ChunkReader(logfile)
parser = SplitParser(reader)

frequency_datastore = {}

period_seconds = 60
ratelimit = 1000
sleep_seconds = 1


def filter_ips(frequency_datastore, treshold):
    for ip in frequency_datastore:
        if frequency_datastore[ip] > treshold:
            pass
            # ban ip

time_now = time()
for ip in parser:

    if not ip:
        sleep(sleep_seconds)
        continue

    try:
        frequency_datastore[ip] += 1 
    except KeyError:
        frequency_datastore[ip] = 1