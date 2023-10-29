# class for get messages of channel by limit
class getMessagesLimit:
    def __init__(self, getChannel):

        '''
        getChannel: channel to get messages
        '''

        # set getChannel
        self.getChannel = getChannel

    # get history messages of channel
    async def getMessagesLimit(self):

        # set initial limit = 1
        limit = 1

        # set condition = True
        condition = True

        # create list of messages
        messages = []

        # while condition is True
        while condition:

            # get messages of channel by limit
            async for message in self.getChannel.history(limit=limit):
                
                # if message content is equal to "Selecione o ano que deseja registrar"
                if message.content == "Selecione O Ano Que Deseja Registrar":

                    # set condition = False
                    condition = False
                    
                    # break loop
                    break

            # increment limit
            limit += 1

        # get messages of channel by limit
        async for message in self.getChannel.history(limit=limit):

            # append message in list of messages
            messages.append(message)

        # return list of messages
        return messages