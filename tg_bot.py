import requests

class TGBotHandler:
    #constructor
    def __init__(self, token):
        self.token = token
        self.url_api_addres = "https://api.telegram.org/bot{}/".format(token)

    #return JSON from API method getUpdates
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        parameters = {'timeout': timeout, 'offset': offset}
        return requests.get(self.url_api_addres + method, parameters).json()['result']

    #return last update from server
    def get_last_updates(self):
        last_update = self.get_updates()
        #return None if no updates!!!
        if(len(last_update) > 0):
            return last_update[-1]
        else:
            return None
    
    #send text message
    def send_text_message(self, chat_id=None, text=' ', reply_to_message_id=None):
        if(reply_to_message_id == None):
            parameters =  {'chat_id': chat_id, 'text': text}
        else:
            parameters = {'chat_id': chat_id, 'text': text,
                          'reply_to_message_id': reply_to_message_id}
        method = 'sendMessage'
        return requests.post(self.url_api_addres + method, parameters)

    #send text message in HTML style
    #supported HTML tags:
    #<b>bold</b>, <strong>bold</strong>
    #<i>italic</i>, <em>italic</em>
    #<a href="URL">inline URL</a>
    #<code>inline fixed-width code</code>
    #<pre>pre-formatted fixed-width code block</pre>
    def send_text_HTML_message(self, chat_id, text, reply_to_message_id=None):
        if(reply_to_message_id == None):
            parameters = {'chat_id': chat_id, 'text': text,
                          'parse_mode': 'HTML'}
        else:
            parameters = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML', 
                          'reply_to_message_id': reply_to_message_id}
        method = 'sendMessage'
        return requests.post(self.url_api_addres + method, parameters)
    #send sticker exist in telegram
    def send_sticker_exist(self, chat_id, sticker_id):
        parameters = {'chat_id': chat_id, 'sticker': sticker_id}
        method = 'sendSticker'
        return requests.post(self.url_api_addres + method, parameters)
    #Other new methods

bot = TGBotHandler("1141692325:AAGkNyHWLZX7HHqXVu_fpHAWT4jThvxqwbU")

def main():
    new_offset = None
    last_update_id = 0
    sticker = 'CAACAgIAAxkBAAODX4RsgdDcrnUdFJgj6r4hZqpCaR0AAusBAAIrLT8Z19gEn7d2ETEbBA'
    while(True):
        bot.get_updates(new_offset)
        last_update = bot.get_last_updates()
        if(last_update != None):
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_name = last_update['message']['chat']['first_name']

            if(last_chat_text.lower() == 'сука'):
                #bot.send_text_message(last_chat_id, 'Сам сука, {}'.format(last_chat_name), last_update['message']['message_id'])
                #bot.send_text_HTML_message(last_chat_id,'<b>bold</b> <strong>bold</strong> <i>italic</i> <em>italic</em> <a href="URL">inline URL</a> <code>inline fixed-width code</code> <pre>pre-formatted fixed-width code block</pre>')
                bot.send_sticker_exist(last_chat_id, sticker)
            else:
                bot.send_text_message(last_chat_id, '5 минут, полёт нормальный')
        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
