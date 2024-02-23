# import SelectWhere class from crud
from components.Selects.InsertData import InsertData
from components.Selects.UpdateData import UpdateData
from database.crud.SelectWhere import SelectWhere


# class DataProcessing for process data
class DataProcessing:

    # constructor
    def __init__(self, registerData, cursor, getChannel):

        # set registerData
        self.registerData = registerData

        # set cursor
        self.cursor = cursor

        # set getChannel
        self.getChannel = getChannel

    # format register data method
    async def formatRegisterData(self):
        # if registerData is not empty, call method insertData or updateData
        if (
            self.registerData["rideShareDate"] != ""
            and self.registerData["goingDriver"] != ""
            and self.registerData["returnDriver"] != ""
        ):

            # select data in table RideShare calling class SelectWhere passing table, columns, cursor, whereColumn, whereValue
            selectData = SelectWhere(
                table="RideShare",
                cursor=self.cursor,
                whereColumn="RideShareDate",
                whereValue=f"'{self.registerData['rideShareDate']}'",
            ).getSelectWhere()

            # if selectData is equal to [] means that data not exists in table RideShare then insert data else update data
            if selectData == []:
                await InsertData(
                    self.registerData, self.cursor, self.getChannel
                ).insertData()
            else:
                await UpdateData(
                    self.registerData, self.cursor, self.getChannel
                ).updateData()
