import unittest
from testrestclient.config import *


class TestConfig(unittest.TestCase):

    def test_analyseUrl_httpHostAndPath(self):
        config = self._getConfigForUrl("http://something.com/abc/def")
        self.assertEqual("http", config.protocol)
        self.assertEqual("something.com", config.host)
        self.assertEqual("abc/def", config.path)
        self.assertEqual(0, len(config.params))

    def test_analyseUrl_httpsHostAndPathAndParams(self):
        config = self._getConfigForUrl("https://something.com/abc/def?param1=abc&param2=def")
        self.assertEqual("https", config.protocol)
        self.assertEqual("something.com", config.host)
        self.assertEqual("abc/def", config.path)
        self.assertEqual(2, len(config.params))
        self.assertEqual("abc", config.params["param1"])
        self.assertEqual("def", config.params["param2"])

    def _getConfigForUrl(self, testUrl):
        return Config(None, testUrl, {}, {}, None)


class TestRestClientConfigParser(unittest.TestCase):

    def test_parseConfig_ValidPost(self):
        configString = """
        GET http://www.johnunknown.com/recognition-config/v1/reasons/all?urlparam=1234&urlparam2=5678
        HEADERS:
        header1=abcd
        header2=cde=fg
        PARAMS:
        param1=efgh
        BODY:
        {
            firstName : "John",
            lastName : "Smith"
        }
        """
        config = RestClientConfigParser().parseConfig(configString)
        self.assertEqual("GET", config.method)
        self.assertEqual("http://www.johnunknown.com/recognition-config/v1/reasons/all?urlparam=1234&urlparam2=5678", config.url)
        self.assertEqual("http", config.protocol)
        self.assertEqual("www.johnunknown.com", config.host)
        self.assertEqual(2, len(config.headers))
        self.assertEqual("abcd", config.headers["header1"])
        self.assertEqual("cde=fg", config.headers["header2"])
        self.assertEqual(3, len(config.params))
        self.assertEqual("1234", config.params["urlparam"])
        self.assertEqual("5678", config.params["urlparam2"])
        self.assertEqual("efgh", config.params["param1"])
        self.assertEqual("{\nfirstName : \"John\",\nlastName : \"Smith\"\n}\n", config.body)
