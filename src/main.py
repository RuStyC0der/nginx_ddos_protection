from iptables import IptablesBlockMethod
from reader import ChunkReader
from parser import SplitParser

logfile = "nginx_test_conf/log/access.log"


banner = IptablesBlockMethod()
reader = ChunkReader(logfile)
parser = SplitParser(reader)

frequency_datastore = {}
ratelimit = 1000 # requests per minute

for ip in reader:
    pass