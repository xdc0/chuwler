#
# Link hop and status tracker
#

import sqlite3, os

class Logwork():
    
    def __init__(filepath):
        # Database location
        self.dbLocation = filepath

    def _dbRead(self):
        # Open the database, if it doesn't exist, create it 
        dblocation = self.dbLocation

        if os.path.isfile(filename):
            self.db = sqlite3.connect(filename)
            return self.db

        db = sqlite3.connect(dblocation)
        self.db = db
        cursor = db.cursor()
        cursor.execute("""BEGIN;
                          CREATE TABLE chuwler_results (
                            base_link text,
                            base_status text,
                            hop_1 text
                            status_1 text
                            hop_2 text
                            status_2 text
                            hop_3 text
                            status_3 text
                            hop_4 text
                            status_4 text
                            hop_5 text
                            status_5 text
                          );
                          CREATE INDEX base_http_status_code ON chuwler_results
                          (base_status);
                          """)
        db.commit()
        return db

    def logHop(self,urlLog):
       
        # Event logger
         
        db = self._dbRead()
        logger = db.cursor()
        # Check if entry exist, if it exist, then add a redirection
        logger.execute("""SELECT base_link FROM chuwler_results WHERE base_link
        ="""+urlLog
        log_link = logger.fetchone()
        if log_link is None:
            logger.execute("""INSERT INTO chuwler_results VALUES (%s, %s)""")

# To do stuff here :)
