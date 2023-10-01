# class to create table in database
class CreateTable:
    def __init__(self, connection):
        # create connection
        self.connection = connection

    # method for create table in database passing cursor
    def createTable(self, cursor):
        # create table if not exists in database
        self.createTable = """CREATE TABLE IF NOT EXISTS RideShare (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            RideShareDate TEXT,
            RideShareDriverGoing TEXT,
            RideShareDriverReturn TEXT,
            RideShareTotalSeats INTEGER
        )"""

        # return cursor execute and call createTable
        return cursor.execute(self.createTable)