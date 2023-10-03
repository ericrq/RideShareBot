import datetime
import discord

# class of select ui componets
class SelectUIComponets:
    def __init__(self, channel, client):
        '''
        channel: channel id
        client: discord client
        '''

        # get channel by channel id
        self.channel = client.get_channel(channel)

        # create list of drivers
        self.driver = [
            "Gabriel Rotine",
            "Rafael Zanon",
            "Arthur Ferreto",
            "Felipe Santos",
        ]

        # create dates
        self.createDates()

        # create views of select
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

    # send views date to channel
    async def sendViewDate(self):
        await self.channel.send(content="-----------------------------------------------------------------",view=self.viewDate)

    # send views going drive to channel
    async def sendViewGoingDrive(self):
        await self.channel.send(view=self.viewGoingDrive)

    # send views return drive to channel
    async def sendViewReturnDrive(self):
        await self.channel.send(view=self.viewReturnDrive)
