# import discord library
import discord

# import crud delete by where
from database.crud.DeleteByWhere import DeleteByWhere

# class for create button delete register by date
class BtnDelete:
    def __init__(self, cursor, selectInstance, getChannel):

        ''' 
        cursor: cursor for database
        selectInstance: instance of class Selects
        getChannel: get channel by channel id
        '''

        # set cursor
        self.cursor = cursor

        # set selectInstance
        self.selectInstance = selectInstance

        # set getChannel
        self.getChannel = getChannel

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
        await self.selectInstance.goingDrive.editViewGoingDrive()
        await self.selectInstance.returnDrive.editViewReturnDrive()

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