# class SelectAll for select all data from table
class SelectAll:
    # constructor
    def __init__(self, table, cursor):
        # create variables for class
        self.table = table
        self.cursor = cursor

        '''
        table: name of table
        cursor: cursor of database
        '''

        # create variable for select all
        self.selectQuery = f"""SELECT * FROM {self.table}"""

        # execute select query
        self.cursor.execute(self.selectQuery)

    # get select all
    def getSelectAll(self):
        # return data
        return self.cursor.fetchall()