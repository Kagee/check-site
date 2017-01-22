FROM selenium/standalone-chrome-debug
MAINTAINER Anders Einar Hilden <hildenae@gmail.com>

VOLUME  [ "/data" ]

RUN apt-get update &&  apt-get -y -q install tcpdump

RUN wget -q https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64.deb
RUN dpkg -i dumb-init_*.deb

COPY selenium_and_tcpdump.sh /opt/bin/selenium_and_tcpdump.sh
RUN chmod +x /opt/bin/selenium_and_tcpdump.sh

# RUN sed -e 's#/bin/bash#/usr/bin/dumb-init /bin/bash#g' -i /opt/bin/entry_point.sh
WORKDIR /tmp
RUN wget -q https://github.com/mitmproxy/mitmproxy/releases/download/v1.0.2/mitmproxy-1.0.2-linux.tar.gz
RUN tar vxf mitmproxy-1.0.2-linux.tar.gz

# Precrate and install mitmdump CA certificate
RUN apt-get update &&  apt-get -y -q install libnss3-tools
RUN timeout 5 ./mitmdump -w /data/outfile --port 8080 --socks --bind-address 127.0.0.1 || true
RUN sudo -u seluser mkdir -p /home/seluser/.pki/nssdb
RUN sudo -u seluser certutil --empty-password -d /home/seluser/.pki/nssdb -N
RUN cp /root/.mitmproxy/mitmproxy-ca.pem /tmp/mitmproxy-ca.pem
RUN chown seluser:seluser /tmp/mitmproxy-ca.pem
RUN sudo -u seluser certutil -d sql:/home/seluser/.pki/nssdb -A -t TC -n "mitmproxy" -i /tmp/mitmproxy-ca.pem

#/usr/sbin/tcpdump
# docker run -d -p 4444:4444 -p 5900:5900 -v /dev/shm:/dev/shm <name>/<tag>
# docker run --net=host -v $PWD:/data corfr/tcpdump -i any -w /data/dump.pcap "icmp"
# docker run -d -p 4444:4444 -p 5900:5900 -v /dev/shm:/dev/shm -v $PWD:/data
# Runs "/usr/bin/dumb-init -- /my/script --with --args"

EXPOSE 5900
EXPOSE 4444

# docker run -d -p 4444:4444 -p 5900:5900 -v /dev/shm:/dev/shm -v $PWD:/data <name>/<tag>
# ENTRYPOINT ["/usr/bin/dumb-init", "--"]
# CMD ["/opt/bin/selenium_and_tcpdump.sh"]
# CMD ["/opt/bin/selenium_and_tcpdump.sh", "--with", "--args"]
# CMD [""]
