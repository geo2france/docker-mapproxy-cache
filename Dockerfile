FROM picnat/mapproxy
ADD run /usr/local/bin/run
ADD config.py /root/config.py
ADD mapproxy.yaml /root/mapproxy.yaml
EXPOSE 80
CMD ["/usr/local/bin/run"]
