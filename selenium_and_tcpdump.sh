#!/usr/bin/dumb-init /bin/bash

TIME_START="$1"
#echo "HELLO ${TIME_START}" >> /data/dump-${TIME_START}.log
/opt/bin/entry_point.sh &
#echo "SELENIUM STARTED" >> 

INTERFACE="$(tcpdump --list-interfaces | grep eth | cut -d'.' -f2 | cut -d' ' -f1)"
NETWORK="$(ip route | grep 'scope link' | cut -d' ' -f 1)"

tcpdump -w /data/dump-${TIME_START}.pcap -i ${INTERFACE} -n "not (src net ${NETWORK} and dst net ${NETWORK}) and not (src net 127.0.0.0/8 and dst net 127.0.0.0/8) and not multicast" 1> /data/dump-${TIME_START}.log 2>/data/dump-${TIME_START}.log 
#echo "ENTRY POINT FISHED" >> /data/dump-${TIME_START}.log
