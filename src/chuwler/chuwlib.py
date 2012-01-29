#
# Need to override the urllib2 to properly
# handle redirects and to log each redirect.
#

import urllib2, httplib, chuwlog

# Define database location, this will be dynamic in the future, for now I use a
# local file for testing purposes.
logger = chuwlog.Logwork("/home/chuy/development/chuwler/testdb.sqlite3")
baseurl = ""

class myHTTPHandler(urllib2.HTTPHandler):

    def __init__(self):
        urllib2.HTTPHandler.__init__(self)
        self.logger = chuwlog.Logwork("/home/chuy/development/chuwler/testdb.sqlite3")
        self.baseurl = ""

# Overriding the httphandler object of urllib for tracking each hop and page
# http status code. That will go into the database using the chuwlog library
    
    def http_open(self, req):

        # Do the request the same way urllib2 originally does

        respond = ""

        try:
            respond = self.do_open(httplib.HTTPConnection, req)
        except urllib2.URLError as e:
            try:
                hopnum = str(len(req.redirect_dict))
                urlog = [req.get_full_url(),e.args[0][1]] 
                self.logger.logHop(urlog,self.baseurl,hopnum)
            
            except:
                self.baseurl = req._Request__original
                self.logger.createEntry(req.get_full_url(),e.args[0][1])
            raise

        try:
            hopnum = str(len(req.redirect_dict))
            urlog = [req.get_full_url(),respond.code] 
            self.logger.logHop(urlog,self.baseurl,hopnum)

        except:
            self.baseurl = req._Request__original
            logger.createEntry(req.get_full_url(),respond.code)

        return respond

class myHTTPSHandler(urllib2.HTTPSHandler):

    def https_open(self, req):
        # Do the request the same way urllib2 originally does
        respond = self.do_open(httplib.HTTPSConnection, req)
        try:
            hopnum = str(len(req.redirect_dict))
            urlog = [req.get_full_url(),respond.code] 
            self.logger.logHop(urlLog,self.baseurl,hopnum)

        except:
            baseurl = req._Request__original
            logger.createEntry(req.get_full_url(),respond.code)

        return respond


class myHTTPDefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    
    def http_error_default(self, req, fp, code, msg, hdrs):
        
# I don't need exceptions for anything, I need to keep track of every status
# code, it's better to define a handler than creating try except blocks for
# each case.

        pass

class myHTTPRedirectHandler(urllib2.HTTPRedirectHandler):

    # Max 5 redirections after considering it's a loop. I'll catch the 6th one
    # and log it accordingly.

    max_redirections = 1

# Build the opener with the modified handlers above.

def createOpener():
    
    opener = urllib2.build_opener(myHTTPHandler,
    myHTTPDefaultErrorHandler,myHTTPSHandler,myHTTPRedirectHandler)
    urllib2.install_opener(opener)

    return urllib2
