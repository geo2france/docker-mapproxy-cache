import requests
import xml.etree.ElementTree as ET
import yaml

class Capabilities:
    def __init__(self, url):
        self.layers = []
        r = requests.get(url+'?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetCapabilities')
        root = ET.fromstring(r.text)
        layers = root.findall('.//Layer')
        for layer in layers:
            name = layer.find('Name')
            if name is not None:
                self.layers.append(name.text)

class Configuration:
    def __init__(self, filename):
        self.yaml = yaml.load(file(filename,'r'))

    def addWMS(self, url):
        capa = Capabilities(url)
        for layer in capa.layers:
            self.yaml['sources']['src_'+layer] = {
                    'type': 'wms',
                    'req': {
                        'url': url,
                        'layers': layer
                    }
            }
            self.yaml['caches']['cache_'+layer] = {
                    'sources': ['src_'+layer,]
            }
            self.yaml['layers'].append({
                    'name': layer,
                    'sources': ['cache_'+layer],
                    'title': "Style "+layer
            })

    def dumpYaml(self):
        return yaml.dump(self.yaml)

conf = Configuration('mapproxy.yaml')
conf.addWMS('http://localhost:8080/service')
print conf.dumpYaml()
