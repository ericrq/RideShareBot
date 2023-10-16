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

# import crud insert
from db.crud.Insert import Insert

# import crud update
from db.crud.Update import Update

# import crud select where
from db.crud.SelectWhere import SelectWhere

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

        # create list of drivers
        self.driver = os.getenv('DriverNames').split(',')
        
        # define locale for language month get by calendar.month_name
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # create list of last 2 years and current year
        self.years = [str(year) for year in range(datetime.date.today().year - 2, datetime.date.today().year + 1)]

        # create list of all months name and number
        self.months = [f"{calendar.month_name[month]} ({str(month).zfill(2)})" for month in range(1, 13)]

        # get current year and selected year
        self.selectedYear = datetime.date.today().year

        # get current month and selected month
        self.selectedMonthNumber = datetime.date.today().month

        # get current date and selected date
        self.selectedDate = datetime.date.today().strftime("%d/%m/%Y")

        # get selected going drive
        self.selectedGoingDrive = ""

        # get selected return drive
        self.selectedReturnDrive = ""

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

        # get register data
        self.registerData = {
            "year": self.selectedYear,
            "month": self.selectedMonthNumber,
            "rideShareDate": self.selectedDate,
            "goingDriver": "",
            "returnDriver": "",
        }

    # create dates
    def createDates(self, month=datetime.date.today().month, year=datetime.date.today().year):

        # get today date basead in month and year
        self.today  = datetime.date(year, month, 1)

        # get first day of month
        self.firstDayOfMonth = self.today.replace(day=1)

        # get last day of month
        self.lastDayOfMonth = self.today.replace(day=calendar.monthrange(self.today.year, self.today.month)[1])

        # create list of dates
        self.dates = [day.strftime("%d/%m/%Y") for day in (self.firstDayOfMonth + datetime.timedelta(days=day) for day in range((self.lastDayOfMonth - self.firstDayOfMonth).days + 1)) if day.weekday() < 5]

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

        # call method formatRegisterData for format register data for insert or update
        await self.formatRegisterData()

        # interaction response defer
        await interaction.response.defer()

        # call method createDates passing selected month number and selected year
        self.createDates(month=int(self.selectedMonthNumber), year=int(self.selectedYear))

        # clean edit view of date select
        self.viewDate.clear_items()

        # call method editViewDate for edit view of date select
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

    # callback of select year
    async def onYearSelect(self, interaction):

        # get selected year in select component
        self.registerData['year'] = self.selectedYear = interaction.data['values'][0]

        # call method formatRegisterData for format register data for insert or update
        await self.formatRegisterData()

        # interaction response defer
        await interaction.response.defer()

        # call method createDates passing selected month number and selected year
        self.createDates(year=int(self.selectedYear), month=int(self.selectedMonthNumber))

        # clean edit view of date select
        self.viewDate.clear_items()

        # call editViewMonth for edit view of month select
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

        self.selectedDate = interaction.data['values'][0]

        self.registerData['rideShareDate'] = interaction.data['values'][0]

        # call method formatRegisterData for format register data for insert or update
        await self.formatRegisterData()

        # interaction response defer
        await interaction.response.defer()

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

        # callback of going drive select
        self.goingDriveSelect.callback = self.onGoingDriveSelect

        # return view
        return self.viewGoingDrive

    # callback of going drive select
    async def onGoingDriveSelect(self, interaction):

        self.selectedGoingDrive = interaction.data['values'][0]

        self.registerData['goingDriver'] = interaction.data['values'][0]

        # call method formatRegisterData for format register data for insert or update
        await self.formatRegisterData()

        # response interaction defer
        await interaction.response.defer()

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

        # callback of return drive select
        self.returnDriveSelect.callback = self.onReturnDriveSelect

        # return view
        return self.viewReturnDrive

    # callback of return drive select
    async def onReturnDriveSelect(self, interaction):

        # get selected return drive in select component
        self.registerData['returnDriver'] = self.selectedReturnDrive = interaction.data['values'][0]

        # call method formatRegisterData for format register data for insert or update
        await self.formatRegisterData()

        # response interaction defer
        await interaction.response.defer()

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

        # callback of select date
        self.datesSelect.callback = self.onDateSelect

        # edit view of date select
        await messageDateSelect.edit(view=self.viewDate)

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

        # callback of going drive select
        self.goingDriveSelect.callback = self.onGoingDriveSelect

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

        # callback of return drive select
        self.returnDriveSelect.callback = self.onReturnDriveSelect

        # edit view of return drive select
        await messageReturnDrive.edit(view=self.viewReturnDrive)

    # get history messages of channel
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

        # send views year and text to channel
        await self.channel.send(f"Selecione O Ano Que Deseja Registrar", view=self.viewYear)

    # send views return month to channel
    async def sendViewMonth(self):

        # send views month and text to channel
        await self.channel.send(f"Selecione O mês Que Deseja Registrar", view=self.viewMonth)

    # send views return date to channel
    async def sendViewDate(self):

        # send views date and text to channel
        await self.channel.send(f"Selecione A Data Que Deseja Registrar", view=self.viewDate)

    # send views going drive to channel
    async def sendViewGoingDrive(self):

        # send views going drive and text to channel
        await self.channel.send(f"Selecione O Motorista De Ida", view=self.viewGoingDrive)

    # send views return drive to channel
    async def sendViewReturnDrive(self):

        # send views return drive and text to channel
        await self.channel.send(f"Selecione O Motorista De Volta", view=self.viewReturnDrive)

    async def formatRegisterData(self):
        # if registerData is not empty, call method insertData or updateData
        if self.registerData['rideShareDate'] != "" and self.registerData['goingDriver'] != "" and self.registerData['returnDriver'] != "":

            # select data in table RideShare calling class SelectWhere passing table, columns, cursor, whereColumn, whereValue
            selectData = SelectWhere(
                table='RideShare',
                cursor=self.cursor,
                whereColumn='RideShareDate',
                whereValue=f"'{self.registerData['rideShareDate']}'"
            ).getSelectWhere()

            # if selectData is equal to [] means that data not exists in table RideShare then insert data else update data
            if selectData == []:
                await self.insertData()
            else:
                await self.updateData()

    # insert data method
    async def insertData(self):

        # try insert data in table RideShare calling class Insert passing table, columns, values, cursor
        try:
            # call class Insert passing table, columns, values, cursor
            Insert(
                table='RideShare',
                columns='RideShareDate, goingDrive, returnDrive',
                values=f"'{self.registerData['rideShareDate']}', '{self.registerData['goingDriver']}', '{self.registerData['returnDriver']}'",
                cursor=self.cursor
            )

            # create embed for success message
            successEmbed = discord.Embed(
                title='Registro realizado com sucesso',
                color=0x00ff00
            )

            # send success message to channel
            await self.channel.send(embed=successEmbed, delete_after=5)

        # except error
        except:

            # create embed for error message
            errorEmbed = discord.Embed(
                title='Erro ao realizar registro',
                color=0xff0000
            )

            # send error message to channel
            await self.channel.send(embed=errorEmbed, delete_after=5)

    # update data method
    async def updateData(self):

        # try update data in table RideShare calling class Insert passing table, columns, values, cursor
        try:
            # call class Update passing table, columns, values, cursor, whereColumn, whereValue
            Update(
                table='RideShare',
                columns='RideShareDate, goingDrive, returnDrive',
                values=f"'{self.registerData['rideShareDate']}', '{self.registerData['goingDriver']}', '{self.registerData['returnDriver']}'",
                cursor=self.cursor,
                whereColumn='RideShareDate',
                whereValue=f"'{self.registerData['rideShareDate']}'"
            )

            # create embed for success message
            successEmbed = discord.Embed(
                title='Registro atualizado com sucesso',
                color=0x00ff00
            )

            # send success message to channel
            await self.channel.send(embed=successEmbed, delete_after=5)
        
        # except error
        except:

            # creatte embed for error message
            errorEmbed = discord.Embed(
                title='Erro ao atualizar registro',
                color=0xff0000
            )

            # send error message to channel
            await self.channel.send(embed=errorEmbed, delete_after=5)

    # get register data
    def getRegisterData(self):

        # return register data
        return self.registerData
    
    # get channel
    def getChannel(self):

        # return channel
        return self.channel