from testrestclient.config import RestClientConfigParser
import http.client, urllib.parse

class RestCall:

    def __init__(self, configString):
        rest_client = RestClientConfigParser()
        self.config = rest_client.parseConfig(configString)

    def makeCall(self):
        conn = self._createConnection(self.config)
        conn.request(self.config.method, "/" + self.config.path)
        r1 = conn.getresponse()
        response = r1.read()
        print(response)

    def _createConnection(self, config):
        if (config.protocol == "http"):
            conn = http.client.HTTPConnection(config.host)
        elif (config.protocol == "https"):
            conn = http.client.HTTPSConnection(config.host)
        else:
            raise Exception("Unknown protocol '%s'", config.protocol)
        return conn


