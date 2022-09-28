from iptables import IptablesBlockMethod
from reader import BatchReader


logfile = "/dev/shm/access.log"


banner = IptablesBlockMethod()
reader = BatchReader(logfile)

datastore = {}

for ip in reader:
