import discord
from SelectUIComponets import SelectUIComponets
from ConnectSQlite import ConnectSQlite

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

channel = 1157069119917674496

registerData = {
        "date" : "",
        "goingDrive" : "",
        "returnDrive" : "",
        "totalSeats" : ""
    }

# quando o bot estiver pronto
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    selectUIComponets =  SelectUIComponets(channel, client)

    await selectUIComponets.sendViewDate()
    await selectUIComponets.sendViewGoingDrive()
    await selectUIComponets.sendViewReturnDrive()

@client.event
async def on_interaction(interaction):
    await interaction.response.defer()

    if isinstance(interaction, discord.Interaction):
        if interaction.data['custom_id'] == 'datesSelect':
            registerData['date'] = interaction.data['values'][0]

        elif interaction.data['custom_id'] == 'goingDriveSelect':
            registerData['goingDrive'] = interaction.data['values'][0]

        elif interaction.data['custom_id'] == 'returnDriveSelect':
            registerData['returnDrive'] = interaction.data['values'][0]

    insertData(registerData)

def insertData(registerData):
    # chamada do banco de dados
    bd = ConnectSQlite('RideShare.sqlite')

    # envia os dados para o banco de dados
    insertData = """INSERT INTO RideShare (
        RideShareDate,
        RideShareDriverGoing,
        RideShareDriverReturn,
        RideShareTotalSeats
    ) VALUES (?, ?, ?, ?)"""

    updateData = """UPDATE RideShare SET 
        RideShareDate = ?,
        RideShareDriverGoing = ?,
        RideShareDriverReturn = ?,
        RideShareTotalSeats = ?
    WHERE RideShareDate = ?"""

    if bd.cursor.execute("SELECT * FROM RideShare WHERE RideShareDate = ?", (registerData['date'],)).fetchone():
        bd.cursor.execute(updateData, (registerData['date'], registerData['goingDrive'], registerData['returnDrive'], registerData['totalSeats'], registerData['date']))
    else:
        bd.cursor.execute(insertData, (registerData['date'], registerData['goingDrive'], registerData['returnDrive'], registerData['totalSeats']))

    bd.connection.commit()

    

    bd.close()

client.run('MTE1NzA2NTcyMTY5MjU1NzMyMw.GADmnz.6fS1PKyg3unO_C9czR5JXPxd25si_Bqjih3uOs')