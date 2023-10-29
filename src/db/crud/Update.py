# class Update for update data in table
class Update:

    # constructor
    def __init__(self, table, columns, values, cursor, whereColumn, whereValue):

        # create variables for class
        self.table = table
        self.columns = columns
        self.values = values
        self.cursor = cursor
        self.whereColumn = whereColumn
        self.whereValue = whereValue

        '''
        table: name of table
        columns: columns of table
        values: values of columns
        cursor: cursor of database
        '''

        # format columns
        columnsStr = ','.join(self.columns.split(','))

        # format values
        valuesStr = ','.join(self.values.split(','))

        # query for update
        self.updateQuery = f"UPDATE {self.table} SET ({columnsStr}) = ({valuesStr}) WHERE ({self.whereColumn}) = ({self.whereValue})"

        # execute query
        self.cursor.execute(self.updateQuery)
        
        # connection commit
        self.cursor.connection.commit()