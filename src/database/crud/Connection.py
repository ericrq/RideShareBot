# import sqlite3 library
import sqlite3

# class connection database sqlite3
class Connection:

    # constructor
    def __init__(self, pathDB):

        '''
        pathDB: path of database (example: src/db/dataBase.db)
        '''

        # create and connection file .sqlite in src/db
        self.connection = sqlite3.connect(pathDB)

        # create cursor
        self.cursor = self.connection.cursor()

        # connection commit
        self.connection.commit()

    # get connection cursor
    def getCursor(self):

        # return cursor of connection
        return self.cursor