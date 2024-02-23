# import discord library
import discord

# import dotenv library
from dotenv import load_dotenv

# import os library
import os

# import select ui componets
from components.Selects.Selects import Selects

# import button ui components
from components.Buttons.SendButtons import SendButtons

# import crud connections
from database.crud.Connection import Connection

# import crud create table
from database.crud.CreateTable import CreateTable

# import app commands from discord library used for slash commands
from discord import app_commands

# load environment variables
load_dotenv()


# class RideShare for create bot
class RideShare(discord.Client):
    # constructor
    def __init__(self, intents, channel, pathBD, ApiKey, discordGuildId):
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

        self.discordGuildId = discordGuildId

        # set cursor getting connection passing pathBD
        self.cursor = Connection(self.pathBD).getCursor()

        # create table RideShare calling class CreateTable passing table, columns, cursor
        CreateTable(
            "RideShare",
            "RideShareDate TEXT, goingDrive TEXT, returnDrive TEXT",
            self.cursor,
        )

    async def startRideShare(self):
        # create object for select ui componets
        self.Selects = Selects(self.channel, self, self.cursor)

        # create object for button ui components
        self.SendButtons = SendButtons(self.channel, self.cursor, self.Selects)

        # call class for send selects
        await self.Selects.sendSelects()

        # call class for send buttons
        await self.SendButtons.sendButtons()

    # method for run bot
    async def on_ready(self):
        # define activity for bot
        await client.change_presence(activity=discord.Game(name="/rideshare"))

        # await until bot is ready
        await self.wait_until_ready()

        # check if synced is false
        if not self.synced:
            # sync slash commands
            await tree.sync(guild=discord.Object(id=self.discordGuildId))

            # set synced to true
            self.synced = True


# main function
if __name__ == "__main__":
    # create variable for intents
    intents = discord.Intents.default()

    # set intents
    intents.message_content = True

    # get channel id
    DiscordChannelId = os.getenv("DiscordChannelId")

    # convert channel id to int
    channel = int(DiscordChannelId)

    # set discord api key using environment variable
    DiscordApiKey = os.getenv("DiscordApiKey")

    # set discord guild id using environment variable
    DiscordGuildId = os.getenv("DiscordGuildId")

    # create object for class RideShare passing intents, channel, registerData, pathBD, ApiKey
    client = RideShare(
        intents, channel, "src/database/RideShare.sqlite", DiscordApiKey, DiscordGuildId
    )

    # create tree object for slash commands
    tree = app_commands.CommandTree(client)

    # create slash command for start RideShare, passing guild and name and description
    @tree.command(
        guild=discord.Object(id=DiscordGuildId),
        name="rideshare",
        description="Start RideShare",
    )

    # create async function for start RideShare
    async def rideShare(interaction: discord.Interaction):
        # send feedback for user that RideShare was started
        await interaction.response.send_message(
            f"RideShare Foi Iniciado!", ephemeral=True
        )

        # call method startRideShare
        await client.startRideShare()

    # run bot
    client.run(DiscordApiKey)
