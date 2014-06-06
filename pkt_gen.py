import sys
import random
import argparse

try:
  from scapy.all import *
except ImportError:
  print "Import Error: need python-scapy library"
  sys.exit()

## TODO options:
### TCP and/or UDP
### Randomize payload size
### Randomize port
### stop at maximum pcap size rather than pkt count


class WildPacketGenerator(object):
    def __init__(self,  path, count = 100):
	self.pktCnt = count
	self.pktWriter = PcapWriter(path, linktype=1, append=True)

    def genRandomIP(self):
	return str(random.randrange(1,254)) + "." + str(random.randrange(1,254)) + \
	    "." + str(random.randrange(1,254)) + "." + str(random.randrange(1,254))  
	  
    def genRandomPort(self):
	return random.randrange(1,65534)
      
    def genRandomPayload(self):
	return 

    def go(self):
        print "generating a bunch = ", self.pktCnt
        i = 0 
	while i < self.pktCnt:
	    tcpPkt = Ether()/ \
		      IP(src=self.genRandomIP(), dst=self.genRandomIP())/ \
		      TCP(sport=self.genRandomPort(), dport=self.genRandomPort())/ \
		      Raw(load=self.genRandomPayload())
	    self.pktWriter.write(tcpPkt)
	    if (i % 10000) == 0: print "count = ", i
	    i+=1

	self.pktWriter.close()


def main():
    parser = argparse.ArgumentParser(description='Generate a bunch of packets that are \
				     unique across (srcIP/dstIP/sport/dport)' )
    parser.add_argument('-f', '--file', help='Output file to write to', required=True)
    
    parser.add_argument('-t', '--num-tcp', type=int, default = 10, help='Number of TCP \
			packets to generate', required=False)
    
    parser.add_argument('-u', '--num-udp', type=int, default = 10, help='Number of UDP \
			packets to generate', required=False)
    args = parser.parse_args()
    
    print "file=", args.file
    print "num tcp=", args.num_tcp
    print "num udp=", args.num_udp
    	
    g = WildPacketGenerator(args.file, args.num_tcp)
    g.go()
    
if __name__ == "__main__":
  main()
