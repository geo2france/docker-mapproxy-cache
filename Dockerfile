FROM ubuntu:trusty
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y locales && localedef -i fr_FR -c -f UTF-8 -A /usr/share/locale/locale.alias fr_FR.UTF-8

RUN apt-get install -y node-carto apache2 python-dev python-pyproj python-pil python-pip libapache2-mod-wsgi libjpeg-dev zlib1g-dev libyaml-dev gnupg python python-mapnik apache2 python-dev  python-pyproj python-pil python-pip libapache2-mod-wsgi python-pyproj python-pil python-pip libapache2-mod-wsgi libjpeg-dev zlib1g-dev libyaml-dev wget unzip git
RUN apt-get install -y python-requests
ENV HOME /root
RUN pip install MapProxy
ADD run /usr/local/bin/run

EXPOSE 80
CMD ["/usr/local/bin/run"]
