# import discord library
import discord

# class GoingDrive for create select of going drive
class GoingDrive:

    # constructor
    def __init__(self, driverNames, selectedGoingDrive, registerData, dataProcessing, getMessagesLimit, getChannel):

        # set driver names
        self.driverNames = driverNames

        # set selected going drive
        self.selectedGoingDrive = selectedGoingDrive

        # set register data
        self.registerData = registerData

        # set data processing
        self.dataProcessing = dataProcessing

        # set get messages limit
        self.getMessagesLimit = getMessagesLimit

        # set channel
        self.getChannel = getChannel

    # create view of going drive select
    def createViewGoingDriveSelect(self):

        # create select of going drive
        self.goingDriveSelect = discord.ui.Select(
            custom_id="goingDriveSelect",
            placeholder="Selecione O Motorista De Ida",
            options=[discord.SelectOption(label=drive) for drive in self.driverNames]
        )

        # create view
        self.viewGoingDrive = discord.ui.View()

        # add select to view
        self.viewGoingDrive.add_item(self.goingDriveSelect)

        # callback of going drive select
        self.goingDriveSelect.callback = self.onGoingDriveSelect

        # return view
        return self.viewGoingDrive

    # callback of going drive select
    async def onGoingDriveSelect(self, interaction):

        self.selectedGoingDrive = interaction.data['values'][0]

        self.registerData['goingDriver'] = interaction.data['values'][0]

        # call method formatRegisterData for format register data for insert or update
        await self.dataProcessing.formatRegisterData()

        # response interaction defer
        await interaction.response.defer()

    # edit view of going drive select use in buttonDeleteRegisterByDate
    async def editViewGoingDrive(self):

        # call method getMessagesLimit for get messages of channel
        messages = await self.getMessagesLimit.getMessagesLimit()

        # loop in messages of channel
        for message in messages:

            # verify if message content is equal to "Selecione O Motorista De Ida"
            if message.content == "Selecione O Motorista De Ida":

                # set message id in variable
                messageGoingDriveId = message.id

        # fetch message by id
        messageGoingDrive = await self.getChannel.fetch_message(messageGoingDriveId)

        # create select of going drive
        self.goingDriveSelect = discord.ui.Select(
            custom_id="goingDriveSelect",
            placeholder="Selecione O Motorista De Ida",
            options=[discord.SelectOption(label=drive) for drive in self.driverNames]
        )

        # create view
        self.viewGoingDrive = discord.ui.View()

        # add select to view
        self.viewGoingDrive.add_item(self.goingDriveSelect)

        # callback of going drive select
        self.goingDriveSelect.callback = self.onGoingDriveSelect

        # edit view of going drive select
        await messageGoingDrive.edit(view=self.viewGoingDrive)