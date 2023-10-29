# import discord library
import discord

# import Insert class from crud
from db.crud.Insert import Insert

# class InsertData
class InsertData:

    # constructor
    def __init__(self, registerData, cursor, getChannel):

        # set registerData
        self.registerData = registerData

        # set cursor
        self.cursor = cursor

        # set getChannel
        self.getChannel = getChannel

    # insert data method
    async def insertData(self):

        # try insert data in table RideShare calling class Insert passing table, columns, values, cursor
        try:
            # call class Insert passing table, columns, values, cursor
            Insert(
                table='RideShare',
                columns='RideShareDate, goingDrive, returnDrive',
                values=f"'{self.registerData['rideShareDate']}', '{self.registerData['goingDriver']}', '{self.registerData['returnDriver']}'",
                cursor=self.cursor
            )

            # create embed for success message
            successEmbed = discord.Embed(
                title='Registro realizado com sucesso',
                color=0x00ff00
            )

            # send success message to channel
            await self.getChannel.send(embed=successEmbed, delete_after=5)

        # except error
        except:

            # create embed for error message
            errorEmbed = discord.Embed(
                title='Erro ao realizar registro',
                color=0xff0000
            )

            # send error message to channel
            await self.getChannel.send(embed=errorEmbed, delete_after=5)