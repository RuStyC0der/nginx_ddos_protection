from time import time, sleep
from iptables import IptablesBlockMethod
from reader import ChunkReader
from parser import SplitParser
from helpers import get_logger, Config

class Model(object):

    frequency_datastore = {}

    def __init__(self, datasource, ban_engine):
        self.datasource = datasource
        self.ban_engine = ban_engine

        config = Config()

        self.period_seconds = config['RATELIMIT_PERIOD_SECONDS']
        self.ratelimit = config['RATELIMIT']
        self.sleep_seconds = config['SLEEP_ON_EMPTY_LOG_SECONDS']



    def calculate_frequency(self):
        time_previous = 0
        time_delta = 0

        for sample in parser:
            if time_delta > self.period_seconds:
                self.filter_ips(frequency_datastore, self.ratelimit)
                frequency_datastore = {}
                time_delta = 0

            if not sample:
                sleep(self.sleep_seconds)
                time_delta += self.sleep_seconds * 1000
                continue

            ip = sample[0]
            timestamp = float(sample[1])

            time_delta += timestamp - time_previous
            time_previous = timestamp

            try:
                frequency_datastore[ip] += 1 
            except KeyError:
                frequency_datastore[ip] = 1

    def filter_ips(self):
        for ip in self.frequency_datastore:
            if self.frequency_datastore[ip] > self.ratelimit:
                self.ban_engine.ban(ip)

if __name__ == '__main__':
    config = Config()

    ban_engine = IptablesBlockMethod()
    reader = ChunkReader(config['SOURCE_LOG_FILE'])
    parser = SplitParser(reader)

    model = Model(datastore=parser, ban_engine=ban_engine)