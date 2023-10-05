# import discord library
import discord

# import dotenv library
from dotenv import load_dotenv

# import os library
import os

# import calendar library
import datetime

# import locale library
import locale

# import select ui componets
from components.Selects import Selects

# import button ui components
from components.Buttons import Buttons

# import crud connections
from db.crud.Connection import Connection

# import crud insert
from db.crud.Insert import Insert

# import crud update
from db.crud.Update import Update

# import crud create table
from db.crud.CreateTable import CreateTable

# import crud select where
from db.crud.SelectWhere import SelectWhere

# import crud delete by where
from db.crud.DeleteByWhere import DeleteByWhere

# import logic operations
from logic.CalculateTotalPerDriver import CalulateTotalPerDriver

# load environment variables
load_dotenv()

# class RideShare for create bot
class RideShare(discord.Client):
    # constructor
    def __init__(self, intents, channel, registerData, pathBD, ApiKey):
        # call constructor of class discord.Client
        super().__init__(intents=intents)

        # create variables for class
        self.channel = channel
        self.registerData = registerData
        self.pathBD = pathBD
        self.ApiKey = ApiKey
        self.cursor = Connection(self.pathBD).getCursor()

        # define locale for language month get by calendar.month_name
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # create table RideShare calling class CreateTable passing table, columns, cursor
        CreateTable('RideShare', 'RideShareDate TEXT, goingDrive TEXT, returnDrive TEXT', self.cursor)

    # method for run bot
    async def on_ready(self):
        # create object for select ui componets
        self.Selects =  Selects(self.channel, self)

        # create object for button ui components
        self.Buttons = Buttons(self.channel, self)

        # send view for select ui componets
        await self.Selects.sendViewMonth()
        await self.Selects.sendViewDate()
        await self.Selects.sendViewGoingDrive()
        await self.Selects.sendViewReturnDrive()

        # call class for get result
        await self.Buttons.sendButtons()

    # method for get interaction
    async def on_interaction(self, interaction):

        # call method onChargeSelects
        await self.onChargeSelects(interaction)

        # call method onButtonClick
        await self.onButtonClick(interaction)

        # set getChannel for get channel method
        self.getChannel = self.get_channel(self.channel)

        # call method formatData
        await self.formatData()

    # on button click method
    async def onButtonClick(self, interaction):

        # if interaction is instance of discord.Interaction
        if isinstance(interaction, discord.Interaction):

            # if interaction.data['custom_id'] is equal to buttonGetResult
            if interaction.data['custom_id'] == 'buttonGetResult':

                # call method buttonGetResult
                await self.buttonGetResult()

            # if interaction.data['custom_id'] is equal to buttonDeleteRegisterByDate
            elif interaction.data['custom_id'] == 'buttonDeleteRegisterByDate':

                # call method buttonDeleteRegisterByDate
                await self.buttonDeleteRegisterByDate()

    # on charge selects method
    async def onChargeSelects(self, interaction):

        # if interaction is instance of discord.Interaction, defer interaction, remove error message
        await interaction.response.defer()

        # if interaction is instance of discord.Interaction, get data
        if isinstance(interaction, discord.Interaction):

            # if interaction.data['custom_id'] is equal to datesSelect, goingDriveSelect, returnDriveSelect, get values
            if interaction.data['custom_id'] == 'datesSelect':
                self.registerData['RideShareDate'] = interaction.data['values'][0]
            elif interaction.data['custom_id'] == 'goingDriveSelect':
                self.registerData['goingDrive'] = interaction.data['values'][0]

            elif interaction.data['custom_id'] == 'returnDriveSelect':
                self.registerData['returnDrive'] = interaction.data['values'][0]

            elif interaction.data['custom_id'] == 'MonthSelect':
                self.registerData['Month'] = interaction.data['values'][0]

    # format data method
    async def formatData(self):

        # if registerData is not empty, call method insertData or updateData
        if self.registerData['RideShareDate'] != "" and self.registerData['goingDrive'] != "" and self.registerData['returnDrive'] != "":

            # select data in table RideShare calling class SelectWhere passing table, columns, cursor, whereColumn, whereValue
            selectData = SelectWhere(
                table='RideShare',
                cursor=self.cursor,
                whereColumn='RideShareDate',
                whereValue=f"'{self.registerData['RideShareDate']}'"
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
            Insert(
                table='RideShare',
                columns='RideShareDate, goingDrive, returnDrive',
                values=f"'{self.registerData['RideShareDate']}', '{self.registerData['goingDrive']}', '{self.registerData['returnDrive']}'",
                cursor=self.cursor
            )

            # send success message to channel
            await self.getChannel.send('Registro realizado com sucesso', delete_after=5)

        # except error
        except:

            # send error message to channel
            await self.getChannel.send('Erro ao realizar registro' , delete_after=5)

    # update data method
    async def updateData(self):

        # try update data in table RideShare calling class Insert passing table, columns, values, cursor
        try:
            Update(
                table='RideShare',
                columns='RideShareDate, goingDrive, returnDrive',
                values=f"'{self.registerData['RideShareDate']}', '{self.registerData['goingDrive']}', '{self.registerData['returnDrive']}'",
                cursor=self.cursor,
                whereColumn='RideShareDate',
                whereValue=f"'{self.registerData['RideShareDate']}'"
            )
            # send success message to channel
            await self.getChannel.send('Registro atualizado com sucesso', delete_after=5)
        
        # except error
        except:
            # send error message to channel
            await self.getChannel.send('Erro ao atualizar registro', delete_after=5)

    # button get result method
    async def buttonGetResult(self):
        # verify if month is not empty
        if self.registerData['Month'] != "":
            # get month name and number by select
            self.month = self.registerData['Month'].split()[1][1:-1]
        else:
            # set month number actual month
            self.month = datetime.date.today().month

        # call class for calculate total per driver
        calulateTotalPerDriver = CalulateTotalPerDriver(self.cursor, self.channel, self, self.month)
        
        await calulateTotalPerDriver.sendSelectTotalPerDriverFormatTable()

    # button delete register by date method
    async def buttonDeleteRegisterByDate(self):

        # clear registerData for delete register
        self.registerData['goingDrive'] = ""
        self.registerData['returnDrive'] = ""
        
        # get date by delete
        DateByDelete = self.registerData['RideShareDate']

        # try delete data in table RideShare calling class DeleteByWhere passing table, cursor, whereColumn, whereValue
        try:
            DeleteByWhere(
                table='RideShare',
                cursor=self.cursor,
                whereColumn='RideShareDate',
                whereValue=f"'{DateByDelete}'"
            )

            # send success message to channel
            await self.getChannel.send('Registro deletado com sucesso', delete_after=5)

        # except error
        except:
            # send error message to channel
            await self.getChannel.send('Erro ao deletar registro' , delete_after=5)

# main function
if __name__ == '__main__':

    # create variable for intents
    intents = discord.Intents.default()

    # set intents
    intents.message_content = True

    # get channel id
    DiscordChannelId = os.getenv('DiscordChannelId')

    # convert channel id to int
    channel = (int(DiscordChannelId))

    # create variable for register data
    registerData = {
        "RideShareDate" : "",
        "goingDrive" : "",
        "returnDrive" : "",
        "Month" : ""
    }

    # get discord api key
    DiscordApiKey = os.getenv('DiscordApiKey')

    # create object for class RideShare passing intents, channel, registerData, pathBD, ApiKey
    client = RideShare(intents, channel, registerData, 'src/db/RideShare.sqlite', DiscordApiKey)
    
    # run bot
    client.run(DiscordApiKey)