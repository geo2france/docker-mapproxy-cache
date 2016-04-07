FROM picnat/mapproxy
ADD run /usr/local/bin/run
ADD config.py /root/config.py
ADD mapproxy.yaml /root/mapproxy.yaml
ADD seed_base.yaml /root/seed_base.yaml
RUN chmod a+rx /usr/local/bin/run /root/config.py
COPY index.html /var/www/html/index.html
RUN chmod a+r /var/www/html/index.html
EXPOSE 80
CMD ["/usr/local/bin/run"]
