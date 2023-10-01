import sqlite3
from db.CreateTable import CreateTable

# class for connect in database
class ConnectSQlite:
    def __init__(self, dbFile):
        # create and connection file .sqlite in src/db
        self.connection = sqlite3.connect('src/db/' + dbFile)

        # create cursor
        self.cursor = self.connection.cursor()

        # call class CreateTable and method createTable passing cursor for create table
        CreateTable(self).createTable(self.cursor)

        # connection commit
        self.connection.commit()
    
    # method for close connection
    def close(self):
        # close connection
        self.connection.close()