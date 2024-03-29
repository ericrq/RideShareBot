# import crud select total per driver operation
from database.crud.SelectTotalPerDriver import SelectTotalPerDriver

# import table2ascii for create table format
from table2ascii import table2ascii as t2a, PresetStyle, Alignment

# import calendar for get name of month
import calendar

# import discord for usage of embed
import discord


# class CalulateTotalPerDriver for calculate total per driver
class CalulateTotalPerDriver:

    # constructor
    def __init__(self, cursor, channel, client, month, year, interaction):
        """
        cursor: cursor of database
        channel: channel of discord
        client: client of discord
        month: month of ride share
        year: year of ride share
        interaction: interaction of discord
        """

        # set cursor
        self.cursor = cursor

        # set channel
        self.channel = channel

        # set month
        self.month = month

        # set year
        self.year = year

        # set client
        self.client = client

        # set interaction
        self.interaction = interaction

        # call class SelectTotalPerDriver and getSelectTotalPerDriver for return data
        self.getSelectTotalPerDriver = SelectTotalPerDriver(
            self.cursor, self.month, self.year
        ).getSelectTotalPerDriver()

    # method for send table of total per driver
    async def sendSelectTotalPerDriverFormatTable(self):

        # verify if getSelectTotalPerDriver is empty
        if self.getSelectTotalPerDriver == []:

            # # send message to channel and delete after 5 seconds

            embed = discord.Embed(
                title="Não há Dados Registrados",
                description=f"Para O Mês De {calendar.month_name[int(self.month)].capitalize()} De {self.year}",
                color=0x00FF00,
            )

            await self.channel.send(embed=embed, delete_after=5)

            return

        # create table format by table2ascii
        formatTable = t2a(
            header=["Nome Do Motorista", "Total De Vezes Que Dirigiu", "Total A Pagar"],
            body=[
                [driverName, totalDrive, totalToPay]
                for driverName, totalDrive, totalToPay in self.getSelectTotalPerDriver
            ],
            style=PresetStyle.thin_compact,
            alignments=[Alignment.LEFT, Alignment.CENTER, Alignment.CENTER],
            cell_padding=1,
        )

        # send table format to chanel in ephemeral using interaction
        await self.interaction.response.send_message(
            f"```\t\t\t\tTabela Relativa Ao Mes De {calendar.month_name[int(self.month)].capitalize()} De {self.year}\n{formatTable}```",
            ephemeral=True,
        )
