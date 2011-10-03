#
# Main executable
#
import mechanize
from lib import chuwlib

class startScrap():
    def __init__(self):

        self.browser = mechanize.Browser()

    def scrapwl(self,url):
        browse = self.browser
        browse.open(url)
        navigate = chuwlib.createOpener()
        navigate.urlopen(url)

        for links in browse.links(url_regex="http|https"):
            print "Now checking %s" % links.url
            try:
                navigate.urlopen(links.url)
            except:
                print "Some exception found"
                pass

if __name__ == '__main__':

    x = startScrap()
    x.scrapwl("http://www.afrigeneas.com/links/")

