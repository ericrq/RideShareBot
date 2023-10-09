# class SelectWhere  for select data from database with where
class SelectWhere:

    # constructor
    def __init__(self, table, cursor, whereColumn, whereValue):

        # create variables for class
        self.table = table
        self.cursor = cursor
        self.whereColumn = whereColumn
        self.whereValue = whereValue

        '''
        table: name of table
        cursor: cursor of database
        whereColumn: column of where
        whereValue: value of where
        '''

        # create variable for select all
        self.selectQuery = f"""SELECT * FROM {self.table} 
        WHERE {self.whereColumn} = {self.whereValue}"""   

        # execute select query
        self.cursor.execute(self.selectQuery)

    # get select where
    def getSelectWhere(self):

        # return data
        return self.cursor.fetchall()