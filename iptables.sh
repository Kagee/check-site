#!/bin/bash

echo "Setting up NAT ipfilter rules"
sudo iptables -t nat -F
echo "Route traffic to port 80 to local port 10080"
sudo iptables -t nat -A PREROUTING -p tcp --dport 80    -j REDIRECT --to-ports 10080
echo "Route traffic to port 443 to local port 10443"
sudo iptables -t nat -A PREROUTING -p tcp --dport 443   -j REDIRECT --to-ports 10443
echo "IP Rules set up"
