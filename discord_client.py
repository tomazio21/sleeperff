import httputil
import json

urls = {
    'discordHttpApi': 'https://discord.com/api/v10/'
}

class DiscordClient:

    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id

    def send_message(self, message):
        url = urls['discordHttpApi'] + 'channels/' + self.channel_id + '/messages' 
        headers = {
            'Authorization': 'Bot ' + self.token,
            'User-Agent': 'DiscordBot',
            'Content-Type': 'application/json'
        }
        message = {'content': message}
        response = httputil.post(url, message, headers)
        return response
