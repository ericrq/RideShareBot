# import discord library
import discord

# import dotenv library
from dotenv import load_dotenv

# import os library
import os

# import create dates class
from components.Selects.CreateDates import CreateDates

# import data processing class
from components.Selects.DataProcessing import DataProcessing

# import getMessagesLimit
from components.Selects.GetMessagesLimit import GetMessagesLimit

# import going drive class
from components.Selects.GoingDrive import GoingDrive

# import return drive class
from components.Selects.ReturnDrive import ReturnDrive

# load environment variables
load_dotenv()

# class of select ui componets
class Selects:

    # constructor
    def __init__(self, channel, client, cursor):

        '''
        channel: channel id
        client: discord client
        cursor: cursor for database
        '''

        # set cursor
        self.cursor = cursor    

        # get channel by channel id
        self.channel = client.get_channel(channel)

        # create instance of class CreateDates
        self.createDates = CreateDates()

        # get current year and selected year
        self.selectedYear = self.createDates.defineActualYear()

        # get current month and selected month
        self.selectedMonthNumber = self.createDates.defineActualMonth()

        # get current date and selected date
        self.selectedDate = self.createDates.defineActualDate()

        # create dates of select date
        self.dates = self.createDates.createDates()

        # create list of drivers
        self.driverNames = os.getenv('DriverNames').split(',')

        # get selected going drive
        self.selectedGoingDrive = ""

        # get selected return drive
        self.selectedReturnDrive = ""

        # get register data
        self.registerData = {
            "year": self.selectedYear,
            "month": self.selectedMonthNumber,
            "rideShareDate": self.selectedDate,
            "goingDriver": "",
            "returnDriver": "",
        }

        # create instance of class dataProcessing
        self.dataProcessing = DataProcessing(self.registerData, self.cursor, self.channel)

        # create instance of class getMessagesLimit
        self.getMessagesLimit = GetMessagesLimit(self.channel)

        # create GoingDrive class
        self.goingDrive = GoingDrive(
            driverNames=self.driverNames,
            selectedGoingDrive=self.selectedGoingDrive,
            registerData=self.registerData,
            dataProcessing=self.dataProcessing,
            getMessagesLimit=self.getMessagesLimit,
            getChannel=self.channel
        )

        # create ReturnDrive class
        self.returnDrive = ReturnDrive(
            driverNames=self.driverNames,
            selectedReturnDrive=self.selectedReturnDrive,
            registerData=self.registerData,
            dataProcessing=self.dataProcessing,
            getMessagesLimit=self.getMessagesLimit,
            getChannel=self.channel
        )

        # create views of select date
        self.viewDate = self.createViewDateSelect()

        # create views of select year
        self.viewYear = self.createViewYearSelect()

        # create views of select month
        self.viewMonth = self.createViewMonthSelect()

        # create views of going drive select
        self.viewGoingDrive = self.goingDrive.createViewGoingDriveSelect()

        # create views of return drive select
        self.viewReturnDrive = self.returnDrive.createViewReturnDriveSelect()

    # create views of select year
    def createViewYearSelect(self):

        # create select of return year
        self.yearSelect = discord.ui.Select(
            custom_id="YearSelect",
            placeholder="Ano Que Deseja Registrar",
            options=[discord.SelectOption(label=year) for year in self.createDates.defineYears()]
        )

        # create view
        self.viewYear = discord.ui.View()

        # add select to view
        self.viewYear.add_item(self.yearSelect)

        # callback of select year
        self.yearSelect.callback = self.onYearSelect

        # return view
        return self.viewYear

    # callback of select year
    async def onYearSelect(self, interaction):

        # set selected year
        self.selectedYear = interaction.data['values'][0]

        # set selected year in select component
        self.registerData['year'] = interaction.data['values'][0]

        # interaction response defer
        await interaction.response.defer()

        # set selected going drive and return drive to empty on change date
        self.registerData['goingDriver'] = ""
        self.registerData['returnDriver'] = ""

        # edit view of going drive select for reseting selected going drive
        await self.goingDrive.editViewGoingDrive()
        await self.returnDrive.editViewReturnDrive()

        # call method formatRegisterData for format register data for insert or update
        await self.dataProcessing.formatRegisterData()

        # call method createDates passing selected month number and selected year
        self.dates = self.createDates.createDates(year=int(self.selectedYear), month=int(self.selectedMonthNumber))

        # clean edit view of date select
        self.viewDate.clear_items()

        # call editViewMonth for edit view of month select
        await self.editViewDate()

    # create views of select month
    def createViewMonthSelect(self):

        # create select of return month
        self.monthSelect = discord.ui.Select(
            custom_id="MonthSelect",
            placeholder="Mês Que Deseja Registrar",
            options=[discord.SelectOption(label=month) for month in self.createDates.defineMonths()]
        )

        # create view
        self.viewMonth = discord.ui.View()

        # add select to view
        self.viewMonth.add_item(self.monthSelect)

        # callback of select month
        self.monthSelect.callback = self.onMonthSelect

        # return view
        return self.viewMonth

    # callback of select month
    async def onMonthSelect(self, interaction):

        # get selected month in select component
        self.selectedMonthData = interaction.data['values'][0]

        # format selected month removing parentheses and getting number
        self.registerData['month'] = self.selectedMonthNumber = self.selectedMonthData.split(' ')[1][1:-1]

        # interaction response defer
        await interaction.response.defer()

        # set selected going drive and return drive to empty on change date
        self.registerData['goingDriver'] = ""
        self.registerData['returnDriver'] = ""

        # edit view of going drive select for reseting selected going drive
        await self.goingDrive.editViewGoingDrive()
        await self.returnDrive.editViewReturnDrive()

        # call method formatRegisterData for format register data for insert or update
        await self.dataProcessing.formatRegisterData()

        # call method createDates passing selected month number and selected year
        self.dates = self.createDates.createDates(year=int(self.selectedYear), month=int(self.selectedMonthNumber))

        # clean edit view of date select
        self.viewDate.clear_items()

        # call method editViewDate for edit view of date select
        await self.editViewDate()

    # create views of select
    def createViewDateSelect(self):

        # create select of dates
        self.datesSelect = discord.ui.Select(
            custom_id="datesSelect",
            placeholder="Selecione A Data",
            options=[discord.SelectOption(label=date) for date in self.dates]
        )

        # create view
        self.viewDate = discord.ui.View()

        # add select to view
        self.viewDate.add_item(self.datesSelect)

        # callback of select date
        self.datesSelect.callback = self.onDateSelect

        # return view
        return self.viewDate

    # callback of select date
    async def onDateSelect(self, interaction):

        # get selected date in select component
        self.selectedDate = interaction.data['values'][0]

        # set register data ride share date with selected date
        self.registerData['rideShareDate'] = interaction.data['values'][0]

        # interaction response defer
        await interaction.response.defer()

        # set selected going drive and return drive to empty on change date
        self.registerData['goingDriver'] = ""
        self.registerData['returnDriver'] = ""

        # edit view of going drive select for reseting selected going drive
        await self.goingDrive.editViewGoingDrive()
        await self.returnDrive.editViewReturnDrive()

        # call method formatRegisterData for format register data for insert or update
        await self.dataProcessing.formatRegisterData()

    #  edit view of date select
    async def editViewDate(self):

        # call method getMessagesLimit for get messages of channel
        messages = await self.getMessagesLimit.getMessagesLimit()

        # loop in messages of channel
        for message in messages:

            # verify if message content is equal to "Selecione A Data Que Deseja Registrar"
            if message.content == "Selecione A Data":

                # set message id in variable
                messageDateId = message.id

        # fetch message by id
        messageDateSelect = await self.channel.fetch_message(messageDateId)

        # create select of dates
        self.datesSelect = discord.ui.Select(
            custom_id="datesSelect",
            placeholder="Selecione A Data",
            options=[discord.SelectOption(label=date) for date in self.dates]
        )

        # create view
        self.viewDate = discord.ui.View()

        # add select to view
        self.viewDate.add_item(self.datesSelect)

        # callback of select date
        self.datesSelect.callback = self.onDateSelect

        # edit view of date select
        await messageDateSelect.edit(view=self.viewDate)

    # method for send selects
    async def sendSelects(self):

        # send views year and text to channel
        await self.channel.send(f"Selecione O Ano", view=self.viewYear)

        # send views month and text to channel
        await self.channel.send(f"Selecione O mês", view=self.viewMonth)

        # send views date and text to channel
        await self.channel.send(f"Selecione A Data", view=self.viewDate)

        # send views going drive and text to channel
        await self.channel.send(f"Selecione O Motorista De Ida", view=self.viewGoingDrive)

        # send views return drive and text to channel
        await self.channel.send(f"Selecione O Motorista De Volta", view=self.viewReturnDrive)

    # get register data
    def getRegisterData(self):

        # return register data
        return self.registerData

    # set register data usage in buttonDeleteRegisterByDate for reseting register data
    def setRegisterData(self):

        # set register data
        self.registerData = {
            "year": self.selectedYear,
            "month": self.selectedMonthNumber,
            "rideShareDate": self.selectedDate,
            "goingDriver": "",
            "returnDriver": "",
        }
    
    # get channel
    def getChannel(self):

        # return channel
        return self.channel