class Config:

    def __init__(self, method, url, headers, params, body):
        self.method = method
        self.url = url
        self.headers = headers
        self.params = params
        self.body = body
        self._analyseUrl()

    def _analyseUrl(self):
        (self.protocol, remaining) = tuple(self.url.split("://"))
        (self.host, remaining) = tuple(remaining.split("/", 1))
        splitPath = remaining.split("?")
        self.path = splitPath[0]

        if (len(splitPath) == 2):
            # split params into dictionary
            urlParams = dict(x.split('=') for x in splitPath[1].split('&'))
            self.params.update(urlParams)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

class RestClientConfigParser:

    # skips empty lines at the beginning of the list and returns remaining list
    def skipEmptyLines(self, lines):
        if (lines[0] == ""):
            return self.skipEmptyLines(lines[1:])
        else:
            return lines

    def parseUrl(self, lines):
        line = lines[0]
        method = line.split(" ")[0]
        url = line.split(" ")[1]
        if (method not in ["GET", "POST", "PUT", "DELETE"]):
            raise Exception("Invalid HTTP method (GET,POST,PUT,DELETE allowed)")
        return (lines[1:], method, url)

    def parseKeysValues(self, lines, parsedValues):
        line = lines[0]
        if "=" in line:
            # this section keeps format of key=value - process it; use first = as separator
            key = line.split("=", 1)[0]
            value = line.split("=", 1)[1]
            parsedValues[key] = value
            (lines, parsedValues) = self.parseKeysValues(lines[1:], parsedValues)
        return (lines, parsedValues)

    def parseKeyValueSection(self, sectionName, lines):
        lines = self.skipEmptyLines(lines)
        actualSectionName = lines[0][:-1]
        if actualSectionName != sectionName:
            raise Exception("Invalid section name: " + actualSectionName)
        return self.parseKeysValues(lines[1:], {})

    def parseBody(self, lines):
        lines = self.skipEmptyLines(lines)
        if (lines[0] != "BODY:"):
            raise Exception("No BODY found")
        return "\n".join(lines[1:])

    # trim spaces
    def cleanLines(self, lines):
        cleanedLines = []
        for line in lines:
            line = line.strip()
            cleanedLines.append(line)
        return cleanedLines

    def parseConfig(self, configString):
        lines = configString.splitlines()
        lines = self.cleanLines(lines)

        # skip empty lines at the beginning
        lines = self.skipEmptyLines(lines)
        # parse type and url
        (lines, method, url) = self.parseUrl(lines)
        # parse headers and params
        (lines, headers) = self.parseKeyValueSection("HEADERS", lines)
        (lines, params) = self.parseKeyValueSection("PARAMS", lines)
        # parse body
        body = self.parseBody(lines)
        config = Config(method, url, headers, params, body)
        return config
