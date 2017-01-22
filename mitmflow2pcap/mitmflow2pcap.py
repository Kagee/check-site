#!/usr/bin/env python3
#
# Simple script showing how to read a mitmproxy dump file
#

from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
import pprint
import sys
from scapy.all import *


ip_mac_map = {}

def ip_to_mac(ip):
	global ip_mac_map
	if ip in ip_mac_map:
		return ip_mac_map[ip]
	
	while True:
		mac = "%01xa:%02x:%02x:%02x:%02x:%02x" % (
			random.randint(0, 15),
		        random.randint(0, 255),
		        random.randint(0, 255),
		        random.randint(0, 255),
		        random.randint(0, 255),
		        random.randint(0, 255)
		        )
		if not mac in ip_mac_map.values():
			print("Mapping %s to mac %s" % (ip, mac))
			ip_mac_map[ip] = mac
			return mac

def EtherIP(srcIP, dstIP):
	return Ether(src=ip_to_mac(srcIP),dst=ip_to_mac(dstIP))/IP(src=srcIP, dst=dstIP)

with open(sys.argv[1], "rb") as logfile:
    freader = io.FlowReader(logfile)
    pp = pprint.PrettyPrinter(indent=4)
    try:
        pkts = []
        cseq=1
        sseq=1000
        #ci, cp, si, sp = ("0.0.0.0","0","0.0.0.0","0")
        client_ports = []
        for f in freader.stream():
            
            server_ip, server_port = f.server_conn.ip_address.address
            client_ip, client_port = f.server_conn.source_address.address
            if server_port == 443:
                # We live about the server port to get rid of a Wireshark warning
                server_port = 80;

            if client_port in client_ports:
                # If the client port is reused, we live about it to get rid of a 
                # Wireshark warning
                client_port = client_ports[-1] + 1;
                client_ports.append(client_port)
            else:
                client_ports.append(client_port)
            print("REQUEST FLOW: %s:%s => %s:%s" % (client_ip, client_port, server_ip, server_port))
            print("-"*100)
            print("\033[92m")
            #request = f.request.method path 
            r=f.request
            REQ="%s %s %s\r\n" % (r.method, r.path, r.http_version)
            for h in r.headers:
                REQ=REQ+"%s: %s\r\n" % (h, f.request.headers[h])
            print(REQ)
            print("")
            REQ=REQ+"\r\n"
            
            bp = bytearray()
            bp.extend(map(ord, REQ))
            bp.extend(r.raw_content)
            
            sys.stdout.flush()
            sys.stdout.buffer.write(r.raw_content)
            sys.stdout.flush()
       
            # Hankshake 
            #SYN (CS)
            pkts.append(EtherIP(client_ip, server_ip)/TCP(sport=client_port,dport=server_port,flags='S', seq=cseq))
            # SYN ACK (SC)
            cseq=cseq+1;
            pkts.append(EtherIP(server_ip, client_ip)/TCP(sport=server_port,dport=client_port,flags='SA',ack=cseq,seq=sseq))
            # ACK (CS)
            sseq=sseq+1;
            pkts.append(EtherIP(client_ip, server_ip)/TCP(sport=client_port,dport=server_port,flags='A',ack=sseq,seq=cseq))
           
            # PSH ACK (CS) Don't increment seq when PSH OR only SYN and FIN increments seq/ack 
            req = EtherIP(client_ip, server_ip)/TCP(sport=client_port,dport=server_port,flags='PA',ack=sseq,seq=cseq)/bytes(bp)
            #pkts.append(EtherIP(client_ip, server_ip)/TCP(sport=client_port,dport=server_port,flags='PA',ack=sseq,seq=cseq)/bytes(b))
            pkts.append(req)
            print(pkts)
            print("\033[00m")
            print("-"*100)
            
            print("RESPONSE FLOW: %s:%s => %s:%s" % (server_ip, server_port, client_ip, client_port))
            print("-"*100)
            print("\033[91m")
            q=f.response
            print("< %s %s %s" % (q.http_version, q.status_code, q.reason))
            RESP="%s %s %s\r\n" % (q.http_version, q.status_code, q.reason)
            for h in q.headers:
                print("< %s: %s" % (h, q.headers[h]))
                RESP=RESP+"%s: %s\r\n" % (h, q.headers[h])
            RESP=RESP+"\r\n"
            print("")

            bq = bytearray()
            bq.extend(map(ord, RESP))
            bq.extend( q.raw_content)
            # PSH ACK (SC)
            #cseq=cseq+1;
            #resp = EtherIP(server_ip,client_ip)/TCP(dport=client_port,sport=server_port,flags='PA',ack=cseq,seq=sseq)/bytes(b)
            cseq=cseq+len(bp);
            resp = TCP(dport=client_port,sport=server_port,flags='PA',ack=cseq,seq=sseq)/bytes(bq)
            #pkts.append(EtherIP(server_ip,client_ip)/TCP(dport=client_port,sport=server_port,flags='PA',ack=cseq,seq=sseq)/bytes(b))
            pkts.append(EtherIP(server_ip,client_ip)/resp)
            # FIN ACK (CS)
            sseq=sseq+len(bq);
            pkts.append(EtherIP(client_ip, server_ip)/TCP(sport=client_port,dport=server_port,flags='FA',ack=sseq,seq=cseq))

            # FIN ACK (SC)
            cseq=cseq+1; # len(bp)+1;
            pkts.append(EtherIP(server_ip, client_ip)/TCP(sport=server_port,dport=client_port,flags='FA',ack=cseq,seq=sseq))

            # ACK (CS)
            sseq=sseq+1;
            pkts.append(EtherIP(client_ip, server_ip)/TCP(sport=client_port,dport=server_port,flags='A',ack=sseq,seq=cseq))

            sseq=sseq+100; cseq=cseq+100;

            sys.stdout.flush()
            sys.stdout.buffer.write(q.content)
            sys.stdout.flush()
            print("\033[00m")
            print("")
            print("-"*100)
            #pp.pprint(f.response.get_state())
            print("")
        wrpcap("temp.pcap",pkts,linktype=1)
    except FlowReadException as e:
        print("Flow file corrupted: {}".format(e))
