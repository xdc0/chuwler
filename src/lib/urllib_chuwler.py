#
# Need to override the urllib2 to properly
# handle redirects and to log each redirect.
#

import urllib2, httplib

class myHTTPHandler(urllib2.HTTPHandler):

# Overriding the httphandler object of urllib for tracking each hop and page
# http status code. That will go into the database using the chuwlog library
    
    def http_open(self, req):
        
        # Do the request the same way urllib2 originally does
        respond = self.do_open(httplib.HTTPConnection, req)

        try:
            url = req.redirect_dict[-1] # This in case a redirection exist
        except:
            url = req.get_full_url()    # This in case it's the first petition
       
        print url
        print respond.code
        return respond


# I create the urllib2 opener here and I'll call it from somewhere else

def createOpener():
    
    opener = urllib2.build_opener(myHTTPHandler)
    urllib2.install_opener(opener)

    return urllib2

# Testing the function
if __name__ == "__main__":

    x = createOpener()
    x.urlopen("http://www.google.net")
