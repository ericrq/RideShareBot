# class SelectTotalPerDriver for selecting total per driver from database
class SelectTotalPerDriver:
    # constructor
    def __init__(self, cursor):
        # create variables for class
        self.cursor = cursor

        '''
        cursor: cursor of database
        '''

        # create variable for select all
        self.selectTotalPerDriverQuery = """
            SELECT driverName, SUM(count) as totalTimesDirected, SUM(count) * 1.5 as totalPay
            FROM (
                SELECT goingDrive as driverName, COUNT(*) as count
                FROM RideShare
                GROUP BY goingDrive
                UNION ALL
                SELECT returnDrive as driverName, COUNT(*) as count
                FROM RideShare
                GROUP BY returnDrive
            ) as subquery
            GROUP BY driverName
            ORDER BY totalPay desc"""
        
        # execute select query
        self.cursor.execute(self.selectTotalPerDriverQuery)

    # get select total per driver
    def getSelectTotalPerDriver(self):
        # return data
        return self.cursor.fetchall()