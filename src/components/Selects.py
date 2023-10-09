# import discord library
import discord

# import calendar library
import calendar

# import locale library
import locale

# import datetime library
import datetime

# import dotenv library
from dotenv import load_dotenv

# import os library
import os

# load environment variables
load_dotenv()

# class of select ui componets
class Selects:
    # constructor
    def __init__(self, channel, client):
        '''
        channel: channel id
        client: discord client
        '''

        # get channel by channel id
        self.channel = client.get_channel(channel)

        # create list of drivers
        self.driver = os.getenv('DriverNames').split(',')
        
        # define locale for language month get by calendar.month_name
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # create list of all months name and number
        self.months = [f"{calendar.month_name[month]} ({str(month).zfill(2)})" for month in range(1, 13)]

        # create list of last 2 years and current year
        self.years = [str(year) for year in range(datetime.date.today().year - 2, datetime.date.today().year + 1)]

        self.selectedYear = datetime.date.today().year

        # create views of select year
        self.viewYear = self.createViewYearSelect()

        # create views of select month
        self.viewMonth = self.createViewMonthSelect()

        # create dates
        self.createDates()

        # create views of select date
        self.viewDate = self.createViewDateSelect()

        # create views of going drive select
        self.viewGoingDrive = self.createViewGoingDriveSelect()

        # create views of return drive select
        self.viewReturnDrive = self.createViewReturnDriveSelect()

    # create dates
    def createDates(self):

        # get today date
        self.today = datetime.date.today()
        
        # get first day of month
        self.firstDayOfMonth = self.today.replace(day=1)

        # get last day of month
        self.lastDayOfMonth = (self.firstDayOfMonth.replace(month=self.firstDayOfMonth.month % 12 + 1, year=self.firstDayOfMonth.year + (1 if self.firstDayOfMonth.month == 12 else 0)) - datetime.timedelta(days=1))

        # create list of dates of month
        self.dates = [dia.strftime("%d/%m/%Y") for dia in (self.firstDayOfMonth + datetime.timedelta(days=d) for d in range((self.lastDayOfMonth - self.firstDayOfMonth).days + 1)) if dia.weekday() < 5]

    # create views of select month
    def createViewMonthSelect(self):

        # create select of return month
        self.monthSelect = discord.ui.Select(
            custom_id="MonthSelect",
            placeholder="Mês Que Deseja Registrar",
            options=[discord.SelectOption(label=month) for month in self.months]
        )

        # create view
        self.viewMonth = discord.ui.View()

        # add select to view
        self.viewMonth.add_item(self.monthSelect)

        self.monthSelect.callback = self.onMonthSelect

        # return view
        return self.viewMonth

    # callback of select month
    async def onMonthSelect(self, interaction):

            # get selected month in select component
            selectedMonth = interaction.data['values'][0]
            
            # transform month name in number
            selectedMonthNumber = self.months.index(selectedMonth) + 1

            # get first day of month
            self.firstDayOfMonth = self.today.replace(day=1,month=selectedMonthNumber)

            # get last day of month
            self.lastDayOfMonth = (self.firstDayOfMonth.replace(month=self.firstDayOfMonth.month % 12 + 1, year=(int(self.selectedYear) + 1 if self.firstDayOfMonth.month == 12 else int(self.selectedYear))) - datetime.timedelta(days=1))

            # get all dates of month
            self.dates = [dia.strftime("%d/%m/%Y") for dia in (self.firstDayOfMonth + datetime.timedelta(days=d) for d in range((self.lastDayOfMonth - self.firstDayOfMonth).days + 1)) if dia.weekday() < 5]

            # edit view of date select
            self.viewDate.clear_items()

            # call method editViewDate for edit view of date select
            await self.editViewDate()

    # callback of select year
    async def onYearSelect(self, interaction):

        # get selected year in select component
        self.selectedYear = interaction.data['values'][0]

        # get first day of month and year
        self.firstDayOfMonth = self.today.replace(day=1, year=int(self.selectedYear))

        # get last day of month and year
        self.lastDayOfMonth = (self.firstDayOfMonth.replace(month=self.firstDayOfMonth.month % 12 + 1, year=(int(self.selectedYear) + 1 if self.firstDayOfMonth.month == 12 else int(self.selectedYear))) - datetime.timedelta(days=1))

        # get all dates based in selected year and month
        self.dates = [dia.strftime("%d/%m/%Y") for dia in (self.firstDayOfMonth + datetime.timedelta(days=d) for d in range((self.lastDayOfMonth - self.firstDayOfMonth).days + 1)) if dia.weekday() < 5]

        # clean edit view of date select
        self.viewDate.clear_items()

        # call editViewMonth for edit view of month select
        await self.editViewDate()

    # create views of select year
    def createViewYearSelect(self):

        # create select of return year
        self.yearSelect = discord.ui.Select(
            custom_id="YearSelect",
            placeholder="Ano Que Deseja Registrar",
            options=[discord.SelectOption(label=year) for year in self.years]
        )

        # create view
        self.viewYear = discord.ui.View()

        # add select to view
        self.viewYear.add_item(self.yearSelect)

        # callback of select year
        self.yearSelect.callback = self.onYearSelect

        # return view
        return self.viewYear
    

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

        # return view
        return self.viewDate

    # create view of going drive select
    def createViewGoingDriveSelect(self):

        # create select of going drive
        self.goingDriveSelect = discord.ui.Select(
            custom_id="goingDriveSelect",
            placeholder="Motorista De Ida",
            options=[discord.SelectOption(label=drive) for drive in self.driver]
        )

        # create view
        self.viewGoingDrive = discord.ui.View()

        # add select to view
        self.viewGoingDrive.add_item(self.goingDriveSelect)

        # return view
        return self.viewGoingDrive
    
    # create view of return drive select
    def createViewReturnDriveSelect(self):

        # create select of return drive
        self.returnDriveSelect = discord.ui.Select(
            custom_id="returnDriveSelect",
            placeholder="Motorista De Volta",
            options=[discord.SelectOption(label=drive) for drive in self.driver]
        )

        # create view
        self.viewReturnDrive = discord.ui.View()

        # add select to view
        self.viewReturnDrive.add_item(self.returnDriveSelect)

        # return view
        return self.viewReturnDrive
    
    # edit view of going drive select use in buttonDeleteRegisterByDate
    async def editViewGoingDrive(self):

        # call method getMessagesLimit for get messages of channel
        messages = await self.getMessagesLimit()

        # loop in messages of channel
        for message in messages:

            # verify if message content is equal to "Selecione O Motorista De Ida"
            if message.content == "Selecione O Motorista De Ida":

                # set message id in variable
                messageGoingDriveId = message.id

        # fetch message by id
        messageGoingDrive = await self.channel.fetch_message(messageGoingDriveId)

        # create select of going drive
        self.goingDriveSelect = discord.ui.Select(
            custom_id="goingDriveSelect",
            placeholder="Motorista De Ida",
            options=[discord.SelectOption(label=drive) for drive in self.driver]
        )

        # create view
        self.viewGoingDrive = discord.ui.View()

        # add select to view
        self.viewGoingDrive.add_item(self.goingDriveSelect)

        # edit view of going drive select
        await messageGoingDrive.edit(view=self.viewGoingDrive)

    # edit view of return drive select use in buttonDeleteRegisterByDate
    async def editViewReturnDrive(self):

        # call method getMessagesLimit for get messages of channel
        messages = await self.getMessagesLimit()

        # loop in messages of channel
        for message in messages:

            # verify if message content is equal to "Selecione O Motorista De Volta"
            if message.content == "Selecione O Motorista De Volta":

                # set message id in variable
                messageReturnDriveId = message.id

        # fetch message by id
        messageReturnDrive = await self.channel.fetch_message(messageReturnDriveId)

        # create select of return drive
        self.returnDriveSelect = discord.ui.Select(
            custom_id="returnDriveSelect",
            placeholder="Motorista De Volta",
            options=[discord.SelectOption(label=drive) for drive in self.driver]
        )

        # create view
        self.viewReturnDrive = discord.ui.View()

        # add select to view
        self.viewReturnDrive.add_item(self.returnDriveSelect)

        # edit view of return drive select
        await messageReturnDrive.edit(view=self.viewReturnDrive)

    #  edit view of date select
    async def editViewDate(self):

        # call method getMessagesLimit for get messages of channel
        messages = await self.getMessagesLimit()

        # loop in messages of channel
        for message in messages:

            # verify if message content is equal to "Selecione A Data Que Deseja Registrar"
            if message.content == "Selecione A Data Que Deseja Registrar":

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

        # edit view of date select
        await messageDateSelect.edit(view=self.viewDate)
    
    async def getMessagesLimit(self):

        # set initial limit = 1
        limit = 1

        # set condition = True
        condition = True

        # create list of messages
        messages = []

        # while condition is True
        while condition:

            # get messages of channel by limit
            async for message in self.channel.history(limit=limit):
                
                # if message content is equal to "Selecione o ano que deseja registrar"
                if message.content == "Selecione O Ano Que Deseja Registrar":

                    # set condition = False
                    condition = False
                    
                    # break loop
                    break

            # increment limit
            limit += 1

        # get messages of channel by limit
        async for message in self.channel.history(limit=limit):

            # append message in list of messages
            messages.append(message)

        # return list of messages
        return messages

    # send views year to channel
    async def sendViewYear(self):
        await self.channel.send(f"Selecione O Ano Que Deseja Registrar", view=self.viewYear)

    # send views return month to channel
    async def sendViewMonth(self):
        await self.channel.send(f"Selecione O mês Que Deseja Registrar", view=self.viewMonth)

    # send views return date to channel
    async def sendViewDate(self):
        await self.channel.send(f"Selecione A Data Que Deseja Registrar", view=self.viewDate)

    # send views going drive to channel
    async def sendViewGoingDrive(self):
        await self.channel.send(f"Selecione O Motorista De Ida", view=self.viewGoingDrive)

    # send views return drive to channel
    async def sendViewReturnDrive(self):
        await self.channel.send(f"Selecione O Motorista De Volta", view=self.viewReturnDrive)