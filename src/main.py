from time import time, sleep
from iptables import IptablesBlockMethod
from reader import ChunkReader
from parser import SplitParser
from helpers import get_logger, Config

logger = get_logger(__name__)

class Model(object):

    frequency_datastore = {}

    def __init__(self, datasource, ban_engine):
        self.datasource = datasource
        self.ban_engine = ban_engine

        config = Config()

        self.period_seconds = float(config['RATELIMIT_PERIOD_SECONDS'])
        self.ratelimit = float(config['RATELIMIT'])
        self.sleep_seconds = float(config['SLEEP_ON_EMPTY_LOG_SECONDS'])

        logger.info('model initialized')



    def calculate_frequency_and_ban(self):
        time_previous = 0
        time_delta = 0

        for sample in parser:
            if time_delta > self.period_seconds:
                logger.info(f"end of time sample reached. filtering results")
                self.filter_ips()
                self.frequency_datastore = {}
                time_delta = 0

            if not sample:
                logger.info(f"end of log file reached. will wait {self.sleep_seconds} seconds")
                sleep(self.sleep_seconds)
                time_delta += self.sleep_seconds * 1000
                continue

            ip = sample[0]
            timestamp = float(sample[1])

            time_delta += timestamp - time_previous
            time_previous = timestamp

            try:
                self.frequency_datastore[ip] += 1 
            except KeyError:
                logger.debug(f"IP {ip} added to datastore first time per time sample")
                self.frequency_datastore[ip] = 1

    def filter_ips(self):
        for ip in self.frequency_datastore:
            if self.frequency_datastore[ip] > self.ratelimit:
                logger.info(f"IP {ip} due to ban")
                self.ban_engine.ban(ip)
                logger.info(f"IP {ip} banned")


if __name__ == '__main__':
    config = Config()

    ban_engine = IptablesBlockMethod()
    reader = ChunkReader(config['SOURCE_LOG_FILE'])
    parser = SplitParser(reader)

    model = Model(datasource=parser, ban_engine=ban_engine)

    model.calculate_frequency_and_ban()