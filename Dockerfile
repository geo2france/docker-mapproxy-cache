FROM ubuntu:trusty
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y locales && localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8

RUN apt-get install -y node-carto apache2 python-dev python-pyproj python-pil python-pip libapache2-mod-wsgi libjpeg-dev zlib1g-dev libyaml-dev gnupg python python-mapnik apache2 python-dev  python-pyproj python-pil python-pip libapache2-mod-wsgi python-pyproj python-pil python-pip libapache2-mod-wsgi libjpeg-dev zlib1g-dev libyaml-dev wget unzip git
RUN apt-get install -y python-requests
RUN useradd -d /srv/mapproxy mapproxy
ENV HOME /root
RUN pip install MapProxy
ADD run /usr/local/bin/run
ADD config.py /root/config.py
ADD mapproxy.yaml /root/mapproxy.yaml
RUN echo "<900913> +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs <>" >> /usr/share/proj/epsg
EXPOSE 80
CMD ["/usr/local/bin/run"]
