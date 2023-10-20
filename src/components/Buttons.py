# import discord library
import discord

# import select ui componets
from components.Selects import Selects

# import crud delete by where
from db.crud.DeleteByWhere import DeleteByWhere

# import logic operations
from logic.CalculateTotalPerDriver import CalulateTotalPerDriver

# class for create button ui components
class Buttons:
    # constructor
    def __init__(self, channel, client, cursor, selectInstance):
        '''
        channel: channel id
        client: discord client
        cursor: cursor for database
        selectInstance: instance of class Selects
        '''

        # set channel
        self.channel = channel

        # set client
        self.client = client

        # set cursor
        self.cursor = cursor

        # set selectInstance
        self.selectInstance = selectInstance

        # get channel by channel id
        self.getChannel = self.selectInstance.getChannel()

        self.registerData = self.selectInstance.getRegisterData()

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
        self.registerData = self.selectInstance.getRegisterData()

        # call class for calculate total per driver
        calulateTotalPerDriver = CalulateTotalPerDriver(self.cursor, self.getChannel, self, self.registerData['month'], self.registerData['year'], interaction)

        # call method for send select total per driver format table
        await calulateTotalPerDriver.sendSelectTotalPerDriverFormatTable()

    # method for create button delete register by date
    def createButtonDeleteRegisterByDate(self):

        # create button delete register by date
        self.buttonDeleteRegisterByDate = discord.ui.Button(
            style=discord.ButtonStyle.red,
            label="Deletar Registros",
            custom_id="buttonDeleteRegisterByDate",
            emoji="🗑️"
        )

        # callback for button delete register by date
        self.buttonDeleteRegisterByDate.callback = self.onClickButtonDeleteRegisterByDate

        # return button delete register by date
        return self.buttonDeleteRegisterByDate
    
    # callback for button delete register by date
    async def onClickButtonDeleteRegisterByDate(self, interaction):

        # defer interaction response
        await interaction.response.defer()

        # call method button delete register by date
        await self.DeleteButtonRegisterByDate()

    # button delete register by date method
    async def DeleteButtonRegisterByDate(self):
        self.registerData = self.selectInstance.getRegisterData()

        # get date by delete
        DateByDelete = self.registerData['rideShareDate']

        if DateByDelete == "":
            return
        
        # call method for edit views usage for reseting views
        await self.selectInstance.editViewReturnDrive()
        await self.selectInstance.editViewGoingDrive()

        # call method for set register data reseting register data
        self.selectInstance.setRegisterData()

        # try delete data in table RideShare calling class DeleteByWhere passing table, cursor, whereColumn, whereValue
        try:
            DeleteByWhere(
                table='RideShare',
                cursor=self.cursor,
                whereColumn='RideShareDate',
                whereValue=f"'{DateByDelete}'"
            )

            # create embed for success message
            successEmbed = discord.Embed(
                title='Registro deletado com sucesso',
                color=0x00ff00
            )

            # send success message to channel
            await self.getChannel.send(embed=successEmbed, delete_after=5)

        # except error
        except:

            # create embed for error message
            errorEmbed = discord.Embed(
                title='Erro ao deletar registro',
                color=0xff0000
            )

            # send error message to channel
            await self.getChannel.send(embed=errorEmbed, delete_after=5)

    # send buttons side by side
    async def sendButtons(self):

        # create view
        self.viewSendButtons = discord.ui.View()

        # add buttons to view
        self.viewSendButtons.add_item(self.createButtonGetResult())
        self.viewSendButtons.add_item(self.createButtonDeleteRegisterByDate())

        # send view to getChannel
        await self.getChannel.send(view=self.viewSendButtons)