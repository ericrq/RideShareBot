# class for insert data in database
class InsertData:
    def __init__(self, bd):
        # create connection
        self.bd = bd

    # method for insert data in database
    def insertData(self, registerData):
        # create variable for register data
        self.registerData = registerData
        
        # create variable for insert data in database
        self.insertRideShare = """INSERT INTO RideShare (
            RideShareDate,
            RideShareDriverGoing,
            RideShareDriverReturn,
            RideShareTotalSeats
        ) VALUES (?, ?, ?, ?)"""

        # create variable for update data in database
        self.updateRideShare = """UPDATE RideShare SET 
            RideShareDate = ?,
            RideShareDriverGoing = ?,
            RideShareDriverReturn = ?,
            RideShareTotalSeats = ?
        WHERE RideShareDate = ?"""

        if self.registerData['date'] == "" and self.registerData['goingDrive'] == "" and self.registerData['returnDrive'] == "" and self.registerData['totalSeats'] == "":
            return

        # if date exists in database, update data, else insert data
        if self.bd.cursor.execute("SELECT * FROM RideShare WHERE RideShareDate = ?", (self.registerData['date'],)).fetchone():
            self.bd.cursor.execute(self.updateRideShare, (self.registerData['date'], self.registerData['goingDrive'], self.registerData['returnDrive'], self.registerData['totalSeats'], self.registerData['date']))
        else:
            self.bd.cursor.execute(self.insertRideShare, (self.registerData['date'], self.registerData['goingDrive'], self.registerData['returnDrive'], self.registerData['totalSeats']))

        # connection commit
        self.bd.connection.commit()

        # close connection
        self.bd.close()
