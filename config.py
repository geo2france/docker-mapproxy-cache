import requests
import xml.etree.ElementTree as ET
import yaml
import sys
import time
import os


class Capabilities:
    def __init__(self, url):
        self.layers = []
        r = requests.get(url + '?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetCapabilities')
        try:
            root = ET.fromstring(r.text.encode('utf8'))
        except:
            sys.stderr.write("Ne peut lire\n")
            sys.stderr.write(r.text.encode('utf8') + "\n")
            sys.exit(2)
        layers = root.findall('.//Layer')
        for layer in layers:
            name = layer.find('Name')
            if name is not None:
                self.layers.append(name.text)


class Configuration:
    def __init__(self, filename):
        self.yaml = yaml.load(file(filename, 'r'))

    def addWMS(self, url):
        capa = Capabilities(url)

        yml_sources = {}
        yml_caches = {}
        yml_layers = []

        for layer in capa.layers:
            yml_sources['src_' + layer] = {
                'type': 'wms',
                'req': {
                    'url': url,
                    'layers': layer
                },
                'http': {
                    'client_timeout': 240,
                    'method': "GET"
                }
            }

            yml_caches['cache_' + layer] = {
                'sources': ['src_' + layer, ],
                'grids': ['cnigl93', 'webmercator'],
                'cache': {
                    'type': 'mongodb',
                    'url': os.getenv('MONGODB_URL')
                },
                'image': {
                    'format': 'image/png',
                    'mode': 'RGBA'
                }
            }

            yml_layers.append({
                'name': layer,
                'sources': ['cache_' + layer],
                'title': "Style " + layer
            })

        self.yaml['sources'] = yml_sources
        self.yaml['caches'] = yml_caches
        self.yaml['layers'] = yml_layers

    def dumpYaml(self):
        return yaml.dump(self.yaml)


conf = Configuration('mapproxy.yaml')
while True:
    try:
        conf.addWMS('http://styles-wms/mapproxy/service')
        break
    except requests.exceptions.ConnectionError:
        sys.stderr.write("WMS service not ready\n")
        time.sleep(1)

print conf.dumpYaml()
