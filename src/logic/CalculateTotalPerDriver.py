# import crud select total per driver operation
from db.crud.SelectTotalPerDriver import SelectTotalPerDriver

# import table2ascii for create table format
from table2ascii import table2ascii as t2a, PresetStyle, Alignment

# class CalulateTotalPerDriver for calculate total per driver
class CalulateTotalPerDriver:
    # constructor
    def __init__(self, cursor, channel, client):
        # create variables for class
        self.cursor = cursor
        self.channel = client.get_channel(channel)

        '''
        cursor: cursor of database
        channel: channel of discord
        '''

        # call class SelectTotalPerDriver and getSelectTotalPerDriver for return data
        self.getSelectTotalPerDriver = SelectTotalPerDriver(self.cursor).getSelectTotalPerDriver()

    # method for send table of total per driver
    async def sendSelectTotalPerDriverFormatTable(self):
        # create table format by table2ascii
        formatTable = t2a(
            header=['Nome Do Motorista', 'Total De Vezes Que Dirigiu', 'Total A Pagar'],
            body=[
                [driverName, totalDrive, totalToPay]
                for driverName, totalDrive, totalToPay in self.getSelectTotalPerDriver
            ],
            style=PresetStyle.thin_compact,
            alignments=[Alignment.LEFT, Alignment.CENTER, Alignment.CENTER],
            cell_padding=1
        )

        # send table format to channel
        await self.channel.send(f'```{formatTable}```')