import tg_bot

bot = tg_bot.TGBotHandler("1141692325:AAGkNyHWLZX7HHqXVu_fpHAWT4jThvxqwbU")

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
            if(bot.get_type_of_message(last_update) == tg_bot.Type_of_message.TEXT):
                last_chat_text = last_update['message']['text']
            elif(bot.get_type_of_message(last_update) == tg_bot.Type_of_message.STICKER):
                bot.send_text_message(last_chat_id, 'you send me sticker')
            elif(bot.get_type_of_message(last_update) == tg_bot.Type_of_message.VOICE):
                bot.send_text_message(last_chat_id, 'you send me voice')
                bot.save_file_by_link(bot.get_file_link(last_update['message']['voice']['file_id']))
            elif(bot.get_type_of_message(last_update) == tg_bot.Type_of_message.DOCUMENT):
                bot.send_text_message(last_chat_id, 'you send me file, nice :)')
                bot.save_file_by_link(bot.get_file_link(last_update['message']['document']['file_id']))
            #last_chat_name = last_update['message']['chat']['first_name']
            #last_chat_message_id = last_update['message']['message_id']
            if(last_chat_text == '/sticker_test' or last_chat_text == '/sticker_test@my_157_test_bot'):
                bot.send_sticker_exist(last_chat_id, sticker)
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
            else:
                bot.send_text_message(last_chat_id, '5 минут, полёт нормальный')
        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
