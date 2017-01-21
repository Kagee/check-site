# HOWTO check-site
1. Install docker, python, selenium for python[1], tshark (and possibly) wireshark, 
2. ./build.sh
3. ./visit "http[s]://example.com"
4. wireshark ./dumps/dump-<x>.pcap -o ssl.keylog_file:./dumps/ssl-key-log-<x>.log
4.1 Add 443 to HTTP (not HTTPS) ports under Edit->Preferences->Protocols->HTTP
4. ./tshark_follow ./dumps/dump-<x>.pcap ./dumps/dump-<x> ./dumps/ssl-key-log-<x>.log # dump ascii
4.1 ./print_follow.py ./dumps/dump-<x>.txt # Print interresting session
[1] http://selenium-python.readthedocs.io/installation.html
