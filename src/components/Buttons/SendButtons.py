# import discord library
import discord

# import btn delete
from components.Buttons.BtnDelete import BtnDelete

# import btn result
from components.Buttons.BtnResult import BtnResult

# class for create button ui components
class SendButtons:
    # constructor
    def __init__(self, channel, cursor, selectInstance):
        '''
        channel: channel id
        cursor: cursor for database
        selectInstance: instance of class Selects
        '''

        # set channel
        self.channel = channel

        # set cursor
        self.cursor = cursor

        # set selectInstance
        self.selectInstance = selectInstance

        # get channel by channel id
        self.getChannel = self.selectInstance.getChannel()

    # send buttons side by side
    async def sendButtons(self):

        # create view
        self.viewSendButtons = discord.ui.View()

        # add buttons to view and create buttons using methods from BtnDelete and BtnResult
        self.viewSendButtons.add_item(BtnResult(self.channel, self.cursor, self.selectInstance).createButtonGetResult())

        self.viewSendButtons.add_item(BtnDelete(self.cursor, self.selectInstance, self.getChannel).createButtonDeleteRegisterByDate())

        # send view to getChannel
        await self.getChannel.send(view=self.viewSendButtons)