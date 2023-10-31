# import discord library
import discord

# class ReturnDrive for create select of return drive
class ReturnDrive:
    def __init__(self, driverNames, selectedReturnDrive, registerData, dataProcessing, getMessagesLimit, getChannel):

        # set driver names
        self.driverNames = driverNames

        # set selected return drive
        self.selectedReturnDrive = selectedReturnDrive

        # set register data
        self.registerData = registerData

        # set data processing
        self.dataProcessing = dataProcessing

        # set get messages limit
        self.getMessagesLimit = getMessagesLimit

        # set channel
        self.getChannel = getChannel

# create view of return drive select
    def createViewReturnDriveSelect(self):

        # create select of return drive
        self.returnDriveSelect = discord.ui.Select(
            custom_id="returnDriveSelect",
            placeholder="Selecione O Motorista De Volta",
            options=[discord.SelectOption(label=drive) for drive in self.driverNames]
        )

        # create view
        self.viewReturnDrive = discord.ui.View()

        # add select to view
        self.viewReturnDrive.add_item(self.returnDriveSelect)

        # callback of return drive select
        self.returnDriveSelect.callback = self.onReturnDriveSelect

        # return view
        return self.viewReturnDrive
    
    # callback of return drive select
    async def onReturnDriveSelect(self, interaction):

        # get selected return drive in select component
        self.registerData['returnDriver'] = self.selectedReturnDrive = interaction.data['values'][0]

        # call method formatRegisterData for format register data for insert or update
        await self.dataProcessing.formatRegisterData()

        # response interaction defer
        await interaction.response.defer()

    # edit view of return drive select use in buttonDeleteRegisterByDate
    async def editViewReturnDrive(self):

        # call method getMessagesLimit for get messages of channel
        messages = await self.getMessagesLimit.getMessagesLimit()

        # loop in messages of channel
        for message in messages:

            # verify if message content is equal to "Selecione O Motorista De Volta"
            if message.content == "Selecione O Motorista De Volta":

                # set message id in variable
                messageReturnDriveId = message.id

        # fetch message by id
        messageReturnDrive = await self.getChannel.fetch_message(messageReturnDriveId)

        # create select of return drive
        self.returnDriveSelect = discord.ui.Select(
            custom_id="returnDriveSelect",
            placeholder="Selecione O Motorista De Volta",
            options=[discord.SelectOption(label=drive) for drive in self.driverNames]
        )

        # create view
        self.viewReturnDrive = discord.ui.View()

        # add select to view
        self.viewReturnDrive.add_item(self.returnDriveSelect)

        # callback of return drive select
        self.returnDriveSelect.callback = self.onReturnDriveSelect

        # edit view of return drive select
        await messageReturnDrive.edit(view=self.viewReturnDrive)