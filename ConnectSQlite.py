import sqlite3

class ConnectSQlite:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
        self.createTable()
    
    def createTable(self):
        create_table = """CREATE TABLE IF NOT EXISTS RideShare (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            RideShareDate TEXT,
            RideShareDriverGoing TEXT,
            RideShareDriverReturn TEXT,
            RideShareTotalSeats INTEGER
        )"""
        
        self.cursor.execute(create_table)
        self.connection.commit()
    
    def close(self):
        self.connection.close()