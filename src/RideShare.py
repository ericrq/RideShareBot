import discord
from components.SelectUIComponets import SelectUIComponets
from dotenv import load_dotenv
import os

from db.crud.Connection import Connection
from db.crud.Insert import Insert
from db.crud.Update import Update
from db.crud.CreateTable import CreateTable
from db.crud.SelectWhere import SelectWhere

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
        # create table RideShare calling class CreateTable passing table, columns, cursor
        CreateTable('RideShare', 'RideShareDate TEXT, goingDrive TEXT, returnDrive TEXT', self.cursor)

    # method for run bot
    async def on_ready(self):
        print(f'Logged in as {self.user}')

        # create object for select ui componets
        selectUIComponets =  SelectUIComponets(self.channel, self)

        # send view for select ui componets
        await selectUIComponets.sendViewMonth()
        await selectUIComponets.sendViewDate()
        await selectUIComponets.sendViewGoingDrive()
        await selectUIComponets.sendViewReturnDrive()

    # method for get interaction
    async def on_interaction(self, interaction):
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

        # set getChannel for get channel method
        self.getChannel = self.get_channel(self.channel)

        # call method formatData
        await self.formatData()

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
            await self.getChannel.send('Registro realizado com sucesso')
        except:
            # send error message to channel
            await self.getChannel.send('Erro ao realizar registro')

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
            await self.getChannel.send('Registro atualizado com sucesso')
        except:
            # send error message to channel
            await self.getChannel.send('Erro ao atualizar registro')

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
        "returnDrive" : ""
    }

    # get discord api key
    DiscordApiKey = os.getenv('DiscordApiKey')

    # create object for class RideShare passing intents, channel, registerData, pathBD, ApiKey
    client = RideShare(intents, channel, registerData, 'src/db/RideShare.sqlite', DiscordApiKey)
    
    # run bot
    client.run(DiscordApiKey)