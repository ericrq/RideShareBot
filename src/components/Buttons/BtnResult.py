# import discord library
import discord

# import logic operations
from components.Buttons.CalculateTotalPerDriver import CalulateTotalPerDriver

class BtnResult:
    def __init__(self, getChannel, cursor, selectInstance):

        '''
        getChannel: get channel by channel id
        cursor: cursor for database
        selectInstance: instance of class Selects
        '''

        # set getChannel
        self.getChannel = getChannel

        # set cursor
        self.cursor = cursor

        # set selectInstance
        self.selectInstance = selectInstance

    # method for create button get result
    def createButtonGetResult(self):

        # create button get result
        self.buttonGetResult = discord.ui.Button(
            style=discord.ButtonStyle.green,
            label="Ver Resultado Do Mes ",
            custom_id="buttonGetResult",
            emoji="📊"
        )

        # callback for button get result
        self.buttonGetResult.callback = self.onClickButtonGetResult

        # return button get result
        return self.buttonGetResult

    # callback for button get result
    async def onClickButtonGetResult(self, interaction):

        # call method buttonGetResult for get result in database
        await self.buttonGetResultSelect(interaction)

    # button get result method
    async def buttonGetResultSelect(self, interaction):

        # get register data from select instance
        self.registerData = self.selectInstance.getRegisterData()

        # call class for calculate total per driver
        calulateTotalPerDriver = CalulateTotalPerDriver(self.cursor, self.getChannel, self, self.registerData['month'], self.registerData['year'], interaction)

        # call method for send select total per driver format table
        await calulateTotalPerDriver.sendSelectTotalPerDriverFormatTable()