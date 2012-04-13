#
# Main executable
#

from chuwler import chuwlib
from lxml import html
import re

class startScrap():

    def __init__(self,baseurl):
        self.baseurl = baseurl.rstrip('/')
        self.setparsedlinks = set ()
        self.navigate = chuwlib.createOpener()

    def parseLinks(self,newLinks):
        """This method cleans the set of links read from the current page
        and compares it with the global set that contains the checked links
        it returns the links that haven't been checked yet"""
        
        return newLinks.difference(self.setparsedlinks)

    def retrieveLinksFromHTML(self,raw_html):
        """This method retrieves the links from the current page, it filters
        all the links on the page and only return these that are either root
        relative or have exactly the same root"""

        rootrelativelinks = raw_html.xpath("//a[starts-with(@href,'/')]/@href")
        otherlinks = raw_html.xpath("//a[re:match(@href,'^[A-Za-z]+.html$')]/@href",namespaces={"re": "http://exslt.org/regular-expressions"})
        linkswithbaseurl = raw_html.xpath("//a[starts-with(@href,'"+self.baseurl+"')]/@href")

        setuniquelinks = set(rootrelativelinks)
        setuniquelinks = setuniquelinks.union(set(otherlinks))

        setuniquelinks = self.sanitizeUrl(setuniquelinks)

        setuniquelinks = setuniquelinks.union(set(linkswithbaseurl))

        return setuniquelinks

    def sanitizeUrl(self,uri_set):
        sanitized = set()
        for uri in uri_set:
            if not re.match("^/",uri):
                uri = "/"+uri
            sanitized.add(self.baseurl+uri)

        return sanitized

    def evaluateLinks(self,setlinkstoevauluate):
        """Evaluates each link given from the argument, the argument is a set
        variable. Everytime it checks a link, it's added on the global set of
        checked links."""

        navigate = self.navigate

        for link in setlinkstoevauluate:
            print "Now checking %s" % link
            try:
                req = navigate.Request(link)
                req.add_header('User-Agent','Mozilla/5.0 (Linux i686)')
                navigate.urlopen(req)
                self.setparsedlinks.add(link)
            except:
                # I need proper exception handling here
                print "Some exception found on url: %s" % link

    def scrapwl(self):
        """Main function to initiate the process, it starts by
        reading the URL and going through all the methods above.
        This need to be further developed, modified, or even removed
        this is intended to be a temporary main method for testing
        the program itself"""

        url = self.baseurl

        navigate = self.navigate
        req = navigate.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Linux i686)')
        render = navigate.urlopen(req)
        #print render.read()
        parse = html.parse(render)

        setlinksforcheck = self.retrieveLinksFromHTML(parse)
        setlinksforcheck = self.parseLinks(setlinksforcheck)
        self.evaluateLinks(setlinksforcheck)


if __name__ == '__main__':
    #url = "http://www.afrigeneas.com"
    #url = "http://bay12games.com/"
    url = "http://www.google.com.mx"
    #url = "http://en.wikipedia.org"
    x = startScrap(url)
    x.scrapwl()
