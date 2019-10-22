import slack
class SlackClient:
    def __init__(self, token):
        self.__client = slack.WebClient(token=token)
    
    # Given the list of channels, return only the PUBLIC channels' ids and names
    def clean_channels_info(self, channels):
        newChannels = []
        for channel in channels:
            if not channel["is_private"]:
                newChannel = {}
                newChannel["id"]=channel["id"]
                newChannel["name"]=channel["name"]
                newChannels.append(newChannel)
        return newChannels

    # Print only the name and the Id of the channels in the given list
    def printChannels(self, channels):
        print("Available channels:")
        for channel in channels:
            print(f'\t{channel["name"]} ({channel["id"]})')

    # Get the channels list and clean it.
    def getChannels(self, show=False):
        response = self.__client.channels_list()
        if response["ok"]:
            channels = response["channels"]
            channels = self.clean_channels_info(channels)
            if show:
                self.printChannels(channels)
            return channels
        print("Error: Couldn't get channels")
        return None

    def clean_messages(self, messages):
        newMessages = []
        for message in messages:
            newMessage = {}
            newMessage["text"] = message["text"]
            newMessage["ts"] = message["ts"]
            newMessages.append(newMessage)
        return newMessages

    # Given a channel ID, return the channel's history of messages
    def getChannelHistory(self, channel_id):
        history_response = self.__client.channels_history(channel=channel_id)
        if history_response["ok"]:
            messages = history_response["messages"]
            messages = self.clean_messages(messages)
            return messages
        print("Error: Couldn't get channel history")
        return None