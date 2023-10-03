# class for creating table in database
class CreateTable:
    # constructor
    def __init__(self, table, columns, cursor):
        # create variables for class
        self.table = table
        self.columns = columns
        self.cursor = cursor

        '''
        tableName: name of table
        columns: columns of table
        cursor: cursor of database
        '''

        # create table query 
        self.createTableQuery = f"""CREATE TABLE IF NOT EXISTS {self.table}(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            {self.columns}
        )"""

        # execute query
        self.cursor.execute(self.createTableQuery)
