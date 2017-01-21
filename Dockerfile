FROM selenium/standalone-chrome-debug
MAINTAINER Anders Einar Hilden <hildenae@gmail.com>

VOLUME  [ "/data" ]

RUN apt-get update &&  apt-get -y -q install tcpdump

RUN wget https://github.com/Yelp/dumb-init/releases/download/v1.2.0/dumb-init_1.2.0_amd64.deb
RUN dpkg -i dumb-init_*.deb

COPY selenium_and_tcpdump.sh /opt/bin/selenium_and_tcpdump.sh
RUN chmod +x /opt/bin/selenium_and_tcpdump.sh

# RUN sed -e 's#/bin/bash#/usr/bin/dumb-init /bin/bash#g' -i /opt/bin/entry_point.sh


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
