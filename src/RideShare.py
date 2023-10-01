import discord
from components.SelectUIComponets import SelectUIComponets
from db.InsertUpdateData import InsertData
from db.ConnectSQlite import ConnectSQlite
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

# class RideShare for create bot
class RideShare(discord.Client):
    # constructor
    def __init__(self, intents, channel, registerData, dbFile, ApiKey):
        # call constructor of class discord.Client
        super().__init__(intents=intents)

        # create variables for class
        self.channel = channel
        self.registerData = registerData
        self.dbFile = dbFile
        self.ApiKey = ApiKey

    # method for run bot
    async def on_ready(self):
        print(f'Logged in as {self.user}')

        # create object for select ui componets
        selectUIComponets =  SelectUIComponets(self.channel, self)

        # send view for select ui componets
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
                self.registerData['date'] = interaction.data['values'][0]

            elif interaction.data['custom_id'] == 'goingDriveSelect':
                self.registerData['goingDrive'] = interaction.data['values'][0]

            elif interaction.data['custom_id'] == 'returnDriveSelect':
                self.registerData['returnDrive'] = interaction.data['values'][0]

        # call class InsertData passing and create db file and insert data
        InsertData(ConnectSQlite(db_file=self.dbFile)).insertData(self.registerData)

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
        "date" : "",
        "goingDrive" : "",
        "returnDrive" : "",
        "totalSeats" : ""
    }

    # get discord api key
    DiscordApiKey = os.getenv('DiscordApiKey')

    # create object for class RideShare passing intents, channel, registerData, dbFile, ApiKey
    client = RideShare(intents, channel, registerData, 'RideShare.sqlite', DiscordApiKey)
    client.run(DiscordApiKey)