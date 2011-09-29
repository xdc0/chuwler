#
# Need to override the urllib2 to properly
# handle redirects and to log each redirect.
#

import urllib2

class myHTTPRedirectHandler(urllib2.HTTPRedirectHandler):

    # Overriding the function to do something when the urllib2 request
    # gets a 301 http status
    def http_error_301(self, req, fp, code, msg, headers):
        
        print code
        print headers

        print "I catch redirections here... Now I need to find a good on how to properly track each hop"

        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    
    # I want this behavior for 301 and 302 only.

    http_error_302 = http_error_301

# I create the urllib2 opener here and I'll call it from somewhere else

def createOpener():
    
    opener = urllib2.build_opener(myHTTPRedirectHandler)
    urllib2.install_opener(opener)

    return urllib2

# Testing the function
if __name__ == "__main__":

    x = createOpener()
    x.urlopen("http://www.google.net")
