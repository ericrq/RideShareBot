# import dotenv library
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# import os library
import os

# class SelectTotalPerDriver for selecting total per driver from database
class SelectTotalPerDriver:

    # constructor
    def __init__(self, cursor, month):

        # create variables for class
        self.cursor = cursor
        self.month = month
        self.valuePerDriver = os.getenv("ValuePerDriver")

        '''
        cursor: cursor of database
        month: month of ride share
        '''

        # create variable for select all per driver and calculate total pay per driver
        self.selectTotalPerDriverQuery = f"""
           SELECT driverName, SUM(count) as totalTimesDirected, SUM(count) * {self.valuePerDriver} as totalPay
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