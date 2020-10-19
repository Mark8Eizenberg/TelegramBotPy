import subprocess
import speech_recognition as sr
import tg_bot as bot
import os
import requests

 #convert oga to ogg
def convert_oga_to_wav(file_path):
    end_file = 'temp.wav'
    subprocess.run(['ffmpeg', '-i', file_path, end_file])
    return end_file

def voice_to_text(voice_file_path):
    r = sr.Recognizer()
    file = sr.AudioFile(voice_file_path)
    with file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        result = r.recognize_google(audio,language='ru')
    return result

tgb = bot.TGBotHandler("1141692325:AAGkNyHWLZX7HHqXVu_fpHAWT4jThvxqwbU")

def main():
    new_offset = None
    last_update_id = 0
    while(True):
        tgb.get_updates(new_offset)
        last_update = tgb.get_last_updates()
        if(last_update != None):
            last_update_id = last_update['update_id']
            last_chat_id = last_update['message']['chat']['id']
            if(tgb.get_type_of_message(last_update) == bot.Type_of_message.VOICE):
                file_from_server = tgb.save_file_by_link(
                    tgb.get_file_link(last_update['message']['voice']['file_id'])) #save file
                new_file = convert_oga_to_wav(file_from_server)
                text_from_voice = voice_to_text(new_file)
                os.remove(file_from_server)
                os.remove(new_file)
                tgb.send_text_message(last_chat_id, "Ваш текст:\n{}".format(text_from_voice))
            elif(tgb.get_type_of_message(last_update) == bot.Type_of_message.TEXT):
                if(last_update['message']['text'].lower() == "/погода" or last_update['message']['text'].lower() == "погода"):
                    weather = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=47.906&lon=33.395&units=metric&exclude=hourly,daily&appid=c32fd26bff44520278bc12f8b3b65878').json()
                    temp = weather['current']['temp']
                    wind = weather['current']['wind_speed']
                    weath = weather['current']['weather'][0]['description']
                    forecast = "Температура: {}\nСкорость ветра: {}\nПогода: {} ".format(temp,wind,weath)
                    tgb.send_text_message(last_chat_id, forecast)
                else:
                    tgb.send_text_message(last_chat_id, "Тебе шо, пообщаться не с кем?")
            else:
                tgb.send_text_message(last_chat_id, "Шо ты мне отправил?")
        new_offset = last_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()

