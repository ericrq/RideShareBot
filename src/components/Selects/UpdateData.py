# import discord library
import discord

# import Update class from crud
from database.crud.Update import Update


# class UpdateData
class UpdateData:

    # constructor
    def __init__(self, registerData, cursor, getChannel):

        # set registerData
        self.registerData = registerData

        # set cursor
        self.cursor = cursor

        # set getChannel
        self.getChannel = getChannel

    # update data method
    async def updateData(self):

        # try update data in table RideShare calling class Insert passing table, columns, values, cursor
        try:
            # call class Update passing table, columns, values, cursor, whereColumn, whereValue
            Update(
                table="RideShare",
                columns="RideShareDate, goingDrive, returnDrive",
                values=f"'{self.registerData['rideShareDate']}', '{self.registerData['goingDriver']}', '{self.registerData['returnDriver']}'",
                cursor=self.cursor,
                whereColumn="RideShareDate",
                whereValue=f"'{self.registerData['rideShareDate']}'",
            )

            # create embed for success message
            successEmbed = discord.Embed(
                title="Registro atualizado com sucesso", color=0x00FF00
            )

            # send success message to channel
            await self.getChannel.send(embed=successEmbed, delete_after=5)

        # except error
        except:

            # creatte embed for error message
            errorEmbed = discord.Embed(
                title="Erro ao atualizar registro", color=0xFF0000
            )

            # send error message to channel
            await self.getChannel.send(embed=errorEmbed, delete_after=5)
