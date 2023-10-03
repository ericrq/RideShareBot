# class for insert data into database
class Insert:
    # constructor
    def __init__(self, table, columns, values, cursor):
        # create variables for class
        self.table = table
        self.columns = columns
        self.values = values
        self.cursor = cursor

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

        # query for insert
        self.insertQuery = f"INSERT INTO {self.table} ({columnsStr}) VALUES ({valuesStr})"

        # execute query
        self.cursor.execute(self.insertQuery)

        # connection commit
        self.cursor.connection.commit()
