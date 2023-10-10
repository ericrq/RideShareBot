# import crud select total per driver operation
from db.crud.SelectTotalPerDriver import SelectTotalPerDriver

# import table2ascii for create table format
from table2ascii import table2ascii as t2a, PresetStyle, Alignment

# import calendar for get name of month
import calendar

# class CalulateTotalPerDriver for calculate total per driver
class CalulateTotalPerDriver:

    # constructor
    def __init__(self, cursor, channel, client, month, year):

        # create variables for class
        self.cursor = cursor
        self.channel = client.get_channel(channel)
        self.month = month
        self.year = year

        '''
        cursor: cursor of database
        channel: channel of discord
        month: month of ride share
        '''

        # call class SelectTotalPerDriver and getSelectTotalPerDriver for return data
        self.getSelectTotalPerDriver = SelectTotalPerDriver(self.cursor, self.month, self.year).getSelectTotalPerDriver()

    # method for send table of total per driver
    async def sendSelectTotalPerDriverFormatTable(self):

        # verify if getSelectTotalPerDriver is empty
        if self.getSelectTotalPerDriver == []:

            # send message to channel and delete after 5 seconds
            await self.channel.send(f'Não há Dados Registrados Para O Mês De {calendar.month_name[int(self.month)].capitalize()} De {self.year}', delete_after=5)
            return

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
        await self.channel.send(f'```\t\t\t\tTabela Relativa Ao Mes De {calendar.month_name[int(self.month)].capitalize()} De {self.year}\n{formatTable}```')