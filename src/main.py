#
# Main executable
#

from chuwler import chuwlib
from lxml import html

class startScrap():

    def __init__(self,baseurl):
        self.baseurl = baseurl
        self.setparsedlinks = set ()

    def parseLinks(self,newLinks):
        """This method cleans the set of links read from the current page
        and compares it with the global set that contains the checked links
        it returns the links that haven't been checked yet"""
        
        return newLinks.difference(self.setparsedlinks)

    def retrieveLinksFromHTML(self,raw_html):
        """This method retrieves the links from the current page, it filters
        all the links on the page and only return these that are either root
        relative or have exactly the same root"""

        setuniquelinks = set()
        
        rootrelativelinks = raw_html.xpath("//a[starts-with(@href,'/')]/@href")
        for index,hrefValue in enumerate(rootrelativelinks):
            rootrelativelinks[index] = self.baseurl+hrefValue

        linkswithbaseurl = raw_html.xpath("//a[starts-with(@href,'"+self.baseurl+"')]/@href")

        setuniquelinks = set(rootrelativelinks)
        setuniquelinks = setuniquelinks.union(set(linkswithbaseurl))

        return setuniquelinks

    def evaluateLinks(self,setlinkstoevauluate):
        """Evaluates each link given from the argument, the argument is a set
        variable. Everytime it checks a link, it's added on the global set of
        checked links."""

        navigate = chuwlib.createOpener()

        for link in setlinkstoevauluate:
            print "Now checking %s" % link
            try:
                navigate.urlopen(link)
                self.setparsedlinks.add(link)
            except:
                # I need proper exception handling here
                print "Some exception found"

    def scrapwl(self):
        """Main function to initiate the process, it starts by
        reading the URL and going through all the methods above.
        This need to be further developed, modified, or even removed
        this is intended to be a temporary main method for testing
        the program itself"""

        url = self.baseurl

        navigate = chuwlib.createOpener()
        render = navigate.urlopen(url)
        parse = html.parse(render)

        setlinksforcheck = self.retrieveLinksFromHTML(parse)
        print str(len(setlinksforcheck)) + " Links found."
        setlinksforcheck = self.parseLinks(setlinksforcheck)
        print str(len(setlinksforcheck)) + " UNIQUE Links found."
        self.evaluateLinks(setlinksforcheck)

if __name__ == '__main__':
    #url = "http://www.afrigeneas.com"
    url = "http://en.wikipedia.org/wiki/Main_Page"
    x = startScrap(url)
    x.scrapwl()
