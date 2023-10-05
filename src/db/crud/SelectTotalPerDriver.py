# class SelectTotalPerDriver for selecting total per driver from database
class SelectTotalPerDriver:
    # constructor
    def __init__(self, cursor, month):
        # create variables for class
        self.cursor = cursor
        self.month = month

        '''
        cursor: cursor of database
        month: month of ride share
        '''

        # create variable for select all per driver query
        self.selectTotalPerDriverQuery = f"""
           SELECT driverName, SUM(count) as totalTimesDirected, SUM(count) * 1.5 as totalPay
            FROM (
                SELECT goingDrive as driverName, COUNT(*) as count
                FROM RideShare
                WHERE substr(RideShareDate, 4, 2) = '{self.month}'
                GROUP BY goingDrive
                UNION ALL
                SELECT returnDrive as driverName, COUNT(*) as count
                FROM RideShare
                WHERE substr(RideShareDate, 4, 2) = '{self.month}'
                GROUP BY returnDrive    
            ) as subquery
            GROUP BY driverName
            ORDER BY totalPay desc
        """
        
        # execute select query
        self.cursor.execute(self.selectTotalPerDriverQuery)

    # get select total per driver
    def getSelectTotalPerDriver(self):
        # return data
        return self.cursor.fetchall()