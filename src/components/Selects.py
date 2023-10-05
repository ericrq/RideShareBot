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

    async def onMonthSelect(self, interaction):
            # get selected month in select component
            selectedMonth = interaction.data['values'][0]
            
            # transform month name in number
            selectedMonthNuber = self.months.index(selectedMonth) + 1

            # get first day of month
            self.firstDayOfMonth = self.today.replace(day=1,month=selectedMonthNuber)

            # get last day of month
            self.lastDayOfMonth = (self.firstDayOfMonth.replace(month=self.firstDayOfMonth.month % 12 + 1, year=self.firstDayOfMonth.year + (1 if self.firstDayOfMonth.month == 12 else 0)) - datetime.timedelta(days=1))

            # get all dates of month
            self.dates = [dia.strftime("%d/%m/%Y") for dia in (self.firstDayOfMonth + datetime.timedelta(days=d) for d in range((self.lastDayOfMonth - self.firstDayOfMonth).days + 1)) if dia.weekday() < 5]

            # edit view of date select
            self.viewDate.clear_items()

            # call method editViewDate for edit view of date select
            await self.editViewDate()

    # create views of select
    def createViewDateSelect(self):
        # create select of dates
        self.datesSelect = discord.ui.Select(
            custom_id="datesSelect",
            placeholder="Selecione a data",
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
            placeholder="Motorista de ida",
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
            placeholder="Motorista de volta",
            options=[discord.SelectOption(label=drive) for drive in self.driver]
        )

        # create view
        self.viewReturnDrive = discord.ui.View()

        # add select to view
        self.viewReturnDrive.add_item(self.returnDriveSelect)

        # return view
        return self.viewReturnDrive

    # send views return month to channel
    async def sendViewMonth(self):
        await self.channel.send(f"Selecione o mês que deseja registrar", view=self.viewMonth)

    #  edit view of date select
    async def editViewDate(self):
        # get last 4 messages of channel
        messages = []
        async for message in self.channel.history(limit=4):
            messages.append(message)

        # get message id date select
        messageDateSelectId = messages[3].id

        # fetch message by id
        messageDateSelect = await self.channel.fetch_message(messageDateSelectId)

        # create select of dates
        self.datesSelect = discord.ui.Select(
            custom_id="datesSelect",
            placeholder="Selecione a data",
            options=[discord.SelectOption(label=date) for date in self.dates]
        )

        # create view
        self.viewDate = discord.ui.View()

        # add select to view
        self.viewDate.add_item(self.datesSelect)

        # edit view of date select
        await messageDateSelect.edit(view=self.viewDate)

    # send views return date to channel
    async def sendViewDate(self):
        await self.channel.send(f"Selecione a data", view=self.viewDate)

    # send views going drive to channel
    async def sendViewGoingDrive(self):
        await self.channel.send(f"Selecione o motorista de ida", view=self.viewGoingDrive)

    # send views return drive to channel
    async def sendViewReturnDrive(self):
        await self.channel.send(f"Slecione o motorista de volta", view=self.viewReturnDrive)
