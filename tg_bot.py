import requests
from enum import Enum
import subprocess

class Type_of_message(Enum):
    TEXT = 1
    STICKER = 2
    AUDIO = 3
    VIDEO = 4
    PHOTO = 5
    DOCUMENT = 6
    VOICE = 7

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
    
    #return true if is private chat, false if group chat
    def is_private_chat(self, last_update_data):
        return (last_update_data['message']['chat']['type'] == 'private')
    
    #type of message
    def get_type_of_message(self, last_update_data):
        if('text' in last_update_data['message']):
            return Type_of_message.TEXT
        elif('sticker' in last_update_data['message']):
            return Type_of_message.STICKER
        elif('audio'in last_update_data['message']):
            return Type_of_message.AUDIO
        elif('video'in last_update_data['message']):
            return Type_of_message.VIDEO
        elif('photo'in last_update_data['message']):
            return Type_of_message.PHOTO
        elif('document'in last_update_data['message']):
            return Type_of_message.DOCUMENT
        elif('voice' in last_update_data['message']):
            return Type_of_message.VOICE
        
    #get file from chat
    def get_file_link(self, file_id):
        parameters = {'file_id':file_id}
        method = 'getFile'
        request = requests.post(self.url_api_addres + method, parameters).json()
        return 'https://api.telegram.org/file/bot{}/'.format(self.token) + request['result']['file_path']
        
<<<<<<< HEAD
    #save file
    def save_file_by_link(self, download_link:str):
        link = requests.get(download_link)
        link_split = download_link.split("/")
        open(link_split[6], 'wb').write(link.content)
        return link_split[6]

    #convert oga to ogg
    def convert_oga_to_ogg(self, file_path):
        end_file = 'temp.ogg'
        subprocess.run(['ffmpeg', '-i', file_path, end_file])
    #Other new methods
=======
#Other new methods
>>>>>>> refs/remotes/origin/main

bot = TGBotHandler("1141692325:AAGkNyHWLZX7HHqXVu_fpHAWT4jThvxqwbU")

greatings = ('привет', 'здравствуй', 'ку', 'здарова', 'здаров', 'хай' )
toSergey = ('/скажи серому', '/серый')
def main():
    new_offset = None
    last_update_id = 0
    sticker = 'CAACAgIAAxkBAAODX4RsgdDcrnUdFJgj6r4hZqpCaR0AAusBAAIrLT8Z19gEn7d2ETEbBA'
    while(True):
        bot.get_updates(new_offset)
        last_update = bot.get_last_updates()
        if(last_update != None):
            last_chat_text = 'text'
            last_update_id = last_update['update_id']
            last_chat_id = last_update['message']['chat']['id']
            if(bot.get_type_of_message(last_update) == Type_of_message.TEXT):
                last_chat_text = last_update['message']['text']
            elif(bot.get_type_of_message(last_update) == Type_of_message.STICKER):
                bot.send_text_message(last_chat_id, 'you send me sticker')
            elif(bot.get_type_of_message(last_update) == Type_of_message.VOICE):
                bot.send_text_message(last_chat_id, 'you send me voice')
                bot.save_file_by_link(bot.get_file_link(last_update['message']['voice']['file_id']))
            elif(bot.get_type_of_message(last_update) == Type_of_message.DOCUMENT):
                bot.send_text_message(last_chat_id, 'you send me file, nice :)')
                bot.save_file_by_link(bot.get_file_link(last_update['message']['document']['file_id']))
            #last_chat_name = last_update['message']['chat']['first_name']
            #last_chat_message_id = last_update['message']['message_id']
            if(last_chat_text == '/sticker_test' or last_chat_text == '/sticker_test@my_157_test_bot'):
                bot.send_sticker_exist(last_chat_id, sticker)
<<<<<<< HEAD
            elif(last_chat_text.lower() == 'test' or last_chat_text.lower() == '/test'):
                #bot.forward_message('', last_chat_id, last_chat_message_id,'true')
                bot.send_full_message(last_chat_id, 'Hi man!', None, None, 'true', last_update['message']['message_id'])
                #bot.send_text_message(last_chat_id, 'Сам сука, {}'.format(last_chat_name), last_update['message']['message_id'])
                #bot.send_text_HTML_message(last_chat_id,'<b>bold</b> <strong>bold</strong> <i>italic</i> <em>italic</em> <code>inline fixed-width code</code> <pre>pre-formatted fixed-width code block</pre> <a href="URL">inline URL</a> ')
                #bot.send_sticker_exist(last_chat_id, sticker)
                #bot.send_photo(last_chat_id, 'AgACAgIAAxkBAAIBCV-Ey_995dZELO37fGFnfHcTtRwqAALjrjEbcg0pSD9tm0F57UKppnFoly4AAwEAAwIAA3kAAzy9AQABGwQ')
                if(bot.is_private_chat(last_update)):
                    bot.send_text_message(last_chat_id, 'it is private')
                else:
                    bot.send_text_message(last_chat_id, 'is group')
=======
            elif(last_chat_text.lower() == 'test'):
                #bot.forward_message(last_chat_id, last_chat_message_id,'true')
                #bot.send_full_message(last_chat_id, 'Hi man!', None, None, 'true', last_update['message']['message_id'])
                #bot.send_text_message(last_chat_id, 'Сам сука, {}'.format(last_chat_name), last_update['message']['message_id'])
                #bot.send_text_HTML_message(last_chat_id,'<b>bold</b> <strong>bold</strong> <i>italic</i> <em>italic</em> <code>inline fixed-width code</code> <pre>pre-formatted fixed-width code block</pre> <a href="URL">inline URL</a> ')
                bot.send_sticker_exist(last_chat_id, sticker)
                #bot.send_photo(last_chat_id, 'AgACAgIAAxkBAAIBCV-Ey_995dZELO37fGFnfHcTtRwqAALjrjEbcg0pSD9tm0F57UKppnFoly4AAwEAAwIAA3kAAzy9AQABGwQ')
            elif(last_chat_text.lower() in greatings):
                bot.send_text_message(last_chat_id, 'Здравствуй, {}'.format(last_chat_name))
            elif(last_chat_text.lower() in toSergey):
                bot.send_text_message(last_chat_id, 'Серый, ты дурак')
>>>>>>> refs/remotes/origin/main
            else:
                bot.send_text_message(last_chat_id, '5 минут, полёт нормальный')
        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
