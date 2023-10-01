import datetime
import discord

class SelectUIComponets:
    def __init__(self, channel, client):
        self.channel = client.get_channel(channel)

        self.driver = [
            "Gabriel Rotine",
            "Rafael Zanon",
            "Arthur Ferreto",
            "Felipe Santos",
        ]

        self.createDates()

        self.viewDate = self.createViewDateSelect()

        self.viewGoingDrive = self.createViewGoingDriveSelect()

        self.viewReturnDrive = self.createViewReturnDriveSelect()

    def createDates(self):
        self.today = datetime.date.today()

        self.firstDayOfMonth = self.today.replace(day=1)

        self.lastDayOfMonth = (self.firstDayOfMonth.replace(month=self.firstDayOfMonth.month % 12 + 1, year=self.firstDayOfMonth.year + (1 if self.firstDayOfMonth.month == 12 else 0)) - datetime.timedelta(days=1))

        # Crie uma lista de datas uteis formatadas
        self.dates = [dia.strftime("%d/%m/%Y") for dia in (self.firstDayOfMonth + datetime.timedelta(days=d) for d in range((self.lastDayOfMonth - self.firstDayOfMonth).days + 1)) if dia.weekday() < 5]

    def createViewDateSelect(self):
        self.datesSelect = discord.ui.Select(
            custom_id="datesSelect",
            placeholder="Selecione a data",
            options=[discord.SelectOption(label=date) for date in self.dates]
        )

        # Crie as views
        self.viewDate = discord.ui.View()
        self.viewDate.add_item(self.datesSelect)

        return self.viewDate

    def createViewGoingDriveSelect(self):
        self.goingDriveSelect = discord.ui.Select(
            custom_id="goingDriveSelect",
            placeholder="Motorista de ida",
            options=[discord.SelectOption(label=drive) for drive in self.driver]
        )

        self.viewGoingDrive = discord.ui.View()
        self.viewGoingDrive.add_item(self.goingDriveSelect)

        return self.viewGoingDrive

    def createViewReturnDriveSelect(self):
        self.returnDriveSelect = discord.ui.Select(
            custom_id="returnDriveSelect",
            placeholder="Motorista de volta",
            options=[discord.SelectOption(label=drive) for drive in self.driver]
        )

        self.viewReturnDrive = discord.ui.View()
        self.viewReturnDrive.add_item(self.returnDriveSelect)

        return self.viewReturnDrive

    async def sendViewDate(self):
        await self.channel.send(view=self.viewDate)

    async def sendViewGoingDrive(self):
        await self.channel.send(view=self.viewGoingDrive)

    async def sendViewReturnDrive(self):
        await self.channel.send(view=self.viewReturnDrive)
