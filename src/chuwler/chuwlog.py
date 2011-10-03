#
# Link hop and status tracker
#

import sqlite3, os

class Logwork():
    
    def __init__(self,filepath):
        # Database location
        self.dbLocation = filepath

    def _dbRead(self):
        # Open the database, if it doesn't exist, create it 
        dblocation = self.dbLocation

        if os.path.isfile(self.dbLocation):
            self.db = sqlite3.connect(self.dbLocation)
            return self.db

        db = sqlite3.connect(dblocation)
        self.db = db
        cursor = db.cursor()
        cursor.executescript("""BEGIN;
                          CREATE TABLE chuwler_results (
                            base_link text,
                            base_status text,
                            hop_1 text,
                            status_1 text,
                            hop_2 text,
                            status_2 text,
                            hop_3 text,
                            status_3 text,
                            hop_4 text,
                            status_4 text,
                            hop_5 text,
                            status_5 text
                          );
                          CREATE INDEX base_http_status_code ON chuwler_results
                          (base_status);
                          COMMIT
                          """)
        db.commit()
        return db

    def logHop(self,urlLog,origurl,hopnum):
       
        # Event logger
        
        # This can't be any uglier
        query = """UPDATE chuwler_results SET hop_%s = '%s', 
                          status_%s = '%s' WHERE
                          base_link = '%s'""" % (hopnum, urlLog[0],
                          hopnum, urlLog[1],origurl)

        db = self._dbRead()
        logger = db.cursor()
        logger.execute(query)
        db.commit()
        db.close()
        return True

    def createEntry(self,url,code):
        
        db = self._dbRead()
        logger = db.cursor()
        logger.execute("""INSERT INTO chuwler_results (base_link, base_status)
        VALUES ('%s', '%s')""" %
        (url,code))
        db.commit()
        db.close()
        return True

# To do stuff here :)

# Testing the function
