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

    #full sendMessage metod
    def send_full_message(self, chat_id, text, parse_mode=None, 
                          disable_web_page_preview=None, disable_notification=None,
                          reply_to_message_id=None, reply_markup=None ):
        parameters = {'chat_id':chat_id, 'text':text}
        if(parse_mode != None):
            parameters += {'parse_mode':parse_mode}
        if(disable_web_page_preview != None):
            parameters['disable_web_page_preview'] = disable_web_page_preview
        if(disable_notification != None):
            parameters['disable_notification'] = disable_notification
        if(reply_to_message_id != None):
            parameters ['reply_to_message_id'] = reply_to_message_id
        if(reply_markup != None):
            parameters['reply_markup'] = reply_markup
        method = 'sendMessage'
        return requests.post(self.url_api_addres + method, parameters)

    #send sticker exist in telegram
    def send_sticker_exist(self, chat_id, sticker_id):
        parameters = {'chat_id': chat_id, 'sticker': sticker_id}
        method = 'sendSticker'
        return requests.post(self.url_api_addres + method, parameters)
    
    #send sticker full method
    def send_sticker(self, chat_id, sticker, disable_notification=None, reply_to_message_id=None,
                     reply_markup=None ):
        parameters = {'chat_id': chat_id, 'sticker': sticker}
        if(disable_notification != None):
            parameters['disable_notification'] = disable_notification
        if(reply_to_message_id != None):
            parameters['reply_to_message_id'] = reply_to_message_id
        if(reply_markup != None):
            parameters['reply_markup'] = reply_markup
        method = 'sendSticker'
        return requests.post(self.url_api_addres + method, parameters)

    #forward message from chat or channel
    #chat_id in format @channel_or_user
    #from_chat_id in format @chanel_or_user or chat_id from result
    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=None):
        parameters = {'chat_id':chat_id, 'from_chat_id':from_chat_id, 'message_id':message_id}
        if(disable_notification != None):
            parameters['disable_notification'] = disable_notification
        method = 'forwardMessage'
        return requests.post(self.url_api_addres + method, parameters)
    
    #send photo to chat
    def send_photo(self, chat_id, photo, caption=None, disable_notification=None, 
                   reply_to_message_id=None, reply_markup=None):
        parameters = {'chat_id': chat_id, 'photo': photo}
        if(caption != None):
            parameters['caption'] = caption
        if(disable_notification != None):
            parameters['disable_notification'] = disable_notification
        if(reply_to_message_id != 'reply_to_message_id'):
            parameters['reply_to_message_id'] = reply_to_message_id
        if(reply_markup != None):
            parameters['reply_markup'] = reply_markup
        method = 'sendPhoto'
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
            #last_chat_name = last_update['message']['chat']['first_name']
            #last_chat_message_id = last_update['message']['message_id']
            if(last_chat_text == '/sticker_test' or last_chat_text == '/sticker_test@my_157_test_bot'):
                bot.send_sticker_exist(last_chat_id, sticker)
            elif(last_chat_text.lower() == 'test'):
                #bot.forward_message('', last_chat_id, last_chat_message_id,'true')
                #bot.send_full_message(last_chat_id, 'Hi man!', None, None, 'true', last_update['message']['message_id'])
                #bot.send_text_message(last_chat_id, 'Сам сука, {}'.format(last_chat_name), last_update['message']['message_id'])
                bot.send_text_HTML_message(last_chat_id,'<b>bold</b> <strong>bold</strong> <i>italic</i> <em>italic</em> <code>inline fixed-width code</code> <pre>pre-formatted fixed-width code block</pre> <a href="URL">inline URL</a> ')
                #bot.send_sticker_exist(last_chat_id, sticker)
                #bot.send_photo(last_chat_id, 'AgACAgIAAxkBAAIBCV-Ey_995dZELO37fGFnfHcTtRwqAALjrjEbcg0pSD9tm0F57UKppnFoly4AAwEAAwIAA3kAAzy9AQABGwQ')
            else:
                bot.send_text_message(last_chat_id, '5 минут, полёт нормальный')
        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
