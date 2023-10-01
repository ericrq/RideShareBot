import discord
from components.SelectUIComponets import SelectUIComponets
from db.InsertUpdateData import InsertData
from db.ConnectSQlite import ConnectSQlite
from dotenv import load_dotenv
import os

load_dotenv()

class RideShare(discord.Client):
    def __init__(self, intents, channel, registerData, dbFile, ApiKey):
        super().__init__(intents=intents)
        self.channel = channel
        self.registerData = registerData
        self.dbFile = dbFile
        self.ApiKey = ApiKey

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        selectUIComponets =  SelectUIComponets(self.channel, self)

        await selectUIComponets.sendViewDate()
        await selectUIComponets.sendViewGoingDrive()
        await selectUIComponets.sendViewReturnDrive()

    async def on_interaction(self, interaction):
        await interaction.response.defer()

        if isinstance(interaction, discord.Interaction):
            if interaction.data['custom_id'] == 'datesSelect':
                self.registerData['date'] = interaction.data['values'][0]

            elif interaction.data['custom_id'] == 'goingDriveSelect':
                self.registerData['goingDrive'] = interaction.data['values'][0]

            elif interaction.data['custom_id'] == 'returnDriveSelect':
                self.registerData['returnDrive'] = interaction.data['values'][0]

        InsertData(ConnectSQlite(db_file=self.dbFile)).insertData(self.registerData)

if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    DiscordChannelId = os.getenv('DiscordChannelId')
    channel = (int(DiscordChannelId))

    registerData = {
        "date" : "",
        "goingDrive" : "",
        "returnDrive" : "",
        "totalSeats" : ""
    }

    DiscordApiKey = os.getenv('DiscordApiKey')

    client = RideShare(intents, channel, registerData, 'RideShare.sqlite', DiscordApiKey)
    client.run(DiscordApiKey)