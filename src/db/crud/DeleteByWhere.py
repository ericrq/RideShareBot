# class for delete by where
class DeleteByWhere:
    # constructor
    def __init__(self, table, cursor, whereColumn, whereValue):
        # create variables for class
        self.cursor = cursor
        self.table = table
        self.whereColumn = whereColumn
        self.whereValue = whereValue

        '''
        table: name of table
        cursor: cursor of database
        whereColumn: column of where
        whereValue: value of where
        '''

        # create variable for delete by date
        self.deleteQuery = f"""DELETE FROM {self.table} 
        WHERE {self.whereColumn} = {self.whereValue}"""

        # execute delete query
        self.cursor.execute(self.deleteQuery)

        # commit changes
        self.cursor.connection.commit()