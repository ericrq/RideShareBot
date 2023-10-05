# import discord library
import discord

# class for create button ui components
class Buttons:
    # constructor
    def __init__(self, channel, client):
        '''
        channel: channel id
        client: discord client
        '''

        # get channel by channel id
        self.channel = client.get_channel(channel)

    # method for create button get result
    def createButtonGetResult(self):
        # create button get result
        self.buttonGetResult = discord.ui.Button(
            style=discord.ButtonStyle.green,
            label="Ver Resultado Do Mes ",
            custom_id="buttonGetResult",
            emoji="📊"
        )

        # return button get result
        return self.buttonGetResult
    
    # method for create button delete register by date
    def createButtonDeleteRegisterByDate(self):
        # create button delete register by date
        self.buttonDeleteRegisterByDate = discord.ui.Button(
            style=discord.ButtonStyle.red,
            label="Deletar Registros",
            custom_id="buttonDeleteRegisterByDate",
            emoji="🗑️"
        )

        # return button delete register by date
        return self.buttonDeleteRegisterByDate
    
    # send buttons side by side
    async def sendButtons(self):
        # create view
        self.viewSendButtons = discord.ui.View()

        # add buttons to view
        self.viewSendButtons.add_item(self.createButtonGetResult())
        self.viewSendButtons.add_item(self.createButtonDeleteRegisterByDate())

        # send view to channel
        await self.channel.send(view=self.viewSendButtons)