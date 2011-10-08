#
# Main executable
#

from chuwler import chuwlib
from lxml import html

setParsedLinks = set()

class startScrap():

    def __init__(self,baseurl):
        self.baseurl = baseurl
        pass

    def parseLinks(self,newLinks):
        """This method cleans the set of links read from the current page
        and compares it with the global set that contains the checked links
        it returns the links that haven't been checked yet"""
        
        global setParsedLinks

        return newLinks.difference(setParsedLinks)

    def retrieveLinksFromHTML(self,raw_html):
        """This method retrieves the links from the current page, it filters
        all the links on the page and only return these that are either root
        relative or have exactly the same root"""

        setUniqueLinks = set()
        
        rootRelativeLinks = raw_html.xpath("//a[starts-with(@href,'/')]/@href")
        for index,hrefValue in enumerate(rootRelativeLinks):
            rootRelativeLinks[index] = self.baseurl+hrefValue

        LinksWithBaseURL = raw_html.xpath("//a[starts-with(@href,'"+self.baseurl+"')]/@href")

        setUniqueLinks = set(rootRelativeLinks)
        setUniqueLinks = setUniqueLinks.union(set(LinksWithBaseURL))

        return setUniqueLinks

    def evaluateLinks(self,setLinksEvaluate):
        """Evaluates each link given from the argument, the argument is a set
        variable. Everytime it checks a link, it's added on the global set of
        checked links."""

        global setParsedLinks

        navigate = chuwlib.createOpener()

        for link in setLinksEvaluate:
            print "Now checking %s" % link
            try:
                navigate.urlopen(link)
                setParsedLinks.add(link)
            except:
                # I need proper exception handling here
                print "Some exception found"
        pass

    def scrapwl(self):
        """Main function to initiate the process, it starts by
        reading the URL and going through all the methods above.
        This need to be further developed, modified, or even removed
        this is intended to be a temporary main method for testing
        the program itself"""

        global setParsedLinks

        url = self.baseurl

        navigate = chuwlib.createOpener()
        renderPage = navigate.urlopen(url)
        HTMLparse = html.parse(renderPage)

        setLinksForCheck = self.retrieveLinksFromHTML(HTMLparse)
        print str(len(setLinksForCheck)) + " Links found."
        setLinksForCheck = self.parseLinks(setLinksForCheck)
        print str(len(setLinksForCheck)) + " UNIQUE Links found."
        self.evaluateLinks(setLinksForCheck)

        pass

if __name__ == '__main__':
    url = "http://www.afrigeneas.com"
    x = startScrap(url)
    x.scrapwl()
