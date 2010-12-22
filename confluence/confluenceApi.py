import xmlrpclib


def singleton(url=None):
    if confluenceApi.singleton is None:
        confluenceApi.singleton = confluenceApi(url)
    return confluenceApi.singleton

def patchXmlrpclibDateConversion():
    def utfEncode(self, out):
        out.write("<value><dateTime.iso8601>")
        out.write(self.value.encode('utf-8'))
        out.write("</dateTime.iso8601></value>\n")
    xmlrpclib.DateTime.encode = utfEncode


class SpaceSummary(object):
    """
    :param key: the space key
    :type key: str
    :param name: the name of the space
    :type key: str
    :param type: type of the space
    :type type: str
    :param url: the url to the view this space online
    :type url: str
    """
    def __init__(self):
        self.key = ''
        self.name = ''
        self.type = ''
        self.url = ''

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.key)

    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return unicode(__str__)

    def display(self, space_summary):
        """Convert the XML-RPC dict to the SpaceSummary class.
        :param space_summary: The XML-RPC dict
        :type space_summary: dict
        """
        self.key = str(space_summary['key'])
        self.name = str(space_summary['name'])
        self.type = str(space_summary['type'])
        self.url = str(space_summary['url'])
        return self

class Space(object):
    """
    :param key: the space key
    :type key: str
    :param name: the name of the space
    :type name: str
    :param url: the url to view this space online
    :type url: str
    :param homepage: the id of the space homepage
    :type homepage: str
    :param description: the HTML rendered space description
    :type description: str
    """
    def __init__(self):
        self.key = ''
        self.name = ''
        self.url = ''
        self.homepage = ''
        self.description = ''

    def __repr__(self):
        return '<%s %r>' % (type(self).__name__, self.key)

    def __str__(self):
        return "%s" % (self.name)

    def __unicode__(self):
        return unicode(__str__)

    def display(self, space):
        """Convert the XML-RPC dict to the Space class.
        :param space: The XML-RPC dict
        :type space: dict
        """
        self.key = str(space['key'])
        self.name = str(space['name'])
        self.type = str(space['type'])
        self.url = str(space['url'])
        self.homepage = str(space['homePage'])
        try:
            self.description = str(space['description'])
        except KeyError:
            self.description = None
        return self

class confluenceApi():

    singleton = None

    def __init__(self, url):
        if url == "":
            return

        self.url = url

    def login(self, username, password):
        self.server = xmlrpclib.ServerProxy(self.url, verbose=True, use_datetime=True, encoding="ASCII")

        try:
            self.token = self.server.confluence1.login(
                username, password)

            return self.token
        except xmlrpclib.Fault, err:
            raise Exception(err.faultString)

    def getSpaces(self):
        try:
            responses = self.server.confluence1.getSpaces(self.token)

            patchXmlrpclibDateConversion()       ### fixing XMLRPC LIB BUG in PYTHON
            spaces = []

            for response in responses:
                print "Spaces: ", [SpaceSummary().display(responses),]

            return spaces
        except xmlrpclib.Fault, err:
            raise Exception(err.faultString)

    def getSpace(self, spaceKey):
        try:
            response = self.server.confluence1.getSpace(self.token, spaceKey)
            space = Space().display(response)

            return space
        except xmlrpclib.Fault, err:
            raise Exception(err.faultString)

    def getPages(self, spaceKey):
        pages = self.server.confluence1.getPages(self.token, spaceKey)
        #return pages['id']

    def getPage(self, spaceKey, pageTitle):
        page = self.server.confluence1.getPage(self.token, spaceKey, pageTitle)
        #return pages['id']

    def getPageById(self, pageId):
        page = self.server.confluence1.getPage(self.token, pageId)
