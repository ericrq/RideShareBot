# import discord library
import discord

# import dotenv library
from dotenv import load_dotenv

# import os library
import os

# import locale library
import locale

# import select ui componets
from components.Selects import Selects

# import button ui components
from components.Buttons import Buttons

# import crud connections
from db.crud.Connection import Connection

# import crud create table
from db.crud.CreateTable import CreateTable

# import crud delete by where
from db.crud.DeleteByWhere import DeleteByWhere

# import app commands from discord library used for slash commands
from discord import app_commands

# load environment variables
load_dotenv()

# class RideShare for create bot
class RideShare(discord.Client):

    # constructor
    def __init__(self, intents, channel, pathBD, ApiKey):

        # call constructor of class discord.Client
        super().__init__(intents=intents)
        
        # set synced to false
        self.synced = False

        # set channel id
        self.channel = channel

        # get channel by id
        self.getChannel = self.get_channel(self.channel)

        # set pathBD
        self.pathBD = pathBD

        # set ApiKey
        self.ApiKey = ApiKey

        # set cursor getting connection passing pathBD
        self.cursor = Connection(self.pathBD).getCursor()

        # define locale for language month get by calendar.month_name
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        # create table RideShare calling class CreateTable passing table, columns, cursor
        CreateTable('RideShare', 'RideShareDate TEXT, goingDrive TEXT, returnDrive TEXT', self.cursor)

    async def startRideShare(self):

        # create object for select ui componets
        self.Selects =  Selects(self.channel, self, self.cursor)

        # create object for button ui components
        self.Buttons = Buttons(self.channel, self, self.cursor, self.Selects)

        # send view for select ui componets
        await self.Selects.sendViewYear()
        await self.Selects.sendViewMonth()
        await self.Selects.sendViewDate()
        await self.Selects.sendViewGoingDrive()
        await self.Selects.sendViewReturnDrive()

        # call class for get result
        await self.Buttons.sendButtons()

    # method for run bot
    async def on_ready(self):

        # await until bot is ready
        await self.wait_until_ready()

        # check if synced is false
        if not self.synced:

            # sync slash commands
            await tree.sync(guild = discord.Object(id=967922108501999616))

            # set synced to true
            self.synced = True

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

    # get discord api key
    DiscordApiKey = os.getenv('DiscordApiKey')

    # create object for class RideShare passing intents, channel, registerData, pathBD, ApiKey
    client = RideShare(intents, channel, 'src/db/RideShare.sqlite', DiscordApiKey)

    # create tree object for slash commands
    tree = app_commands.CommandTree(client)

    # create slash command for start RideShare, passing guild and name and description
    @tree.command(guild = discord.Object(id=967922108501999616), name = 'start', description='Start RideShare')

    # create async function for start RideShare
    async def rideShare(interaction: discord.Interaction):

        # send feedback for user that RideShare was started
        await interaction.response.send_message(f"RideShare Foi Iniciado!", ephemeral=True)

        # call method startRideShare
        await client.startRideShare()

    # run bot
    client.run(DiscordApiKey)