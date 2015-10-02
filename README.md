# docker-mapproxy-cache

docker build -t geopic-cache git://github.com/ndamiens/docker-geopic-cache
docker run -d -p 8081:80 --name "geopic-cache" --link geopic-mapnik:styles-wms geopic-cache
