import subprocess
import speech_recognition as sr
import tg_bot as bot
import os
import platform
import requests

ffmpeg_path = 'ffmpeg'
if(platform.system() == 'Windows'):
    ffmpeg_path = 'C:/ffmpeg/bin/ffmpeg.exe'
 #convert oga to ogg
def convert_oga_to_wav(file_path):
    end_file = 'temp.wav'
    subprocess.run([ffmpeg_path, '-i', file_path, end_file])
    return end_file

def voice_to_text(voice_file_path):
    r = sr.Recognizer()
    file = sr.AudioFile(voice_file_path)
    with file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        result = r.recognize_google(audio,language='ru')
    return result

def get_weather_str():
    weather = requests.get('https://api.openweathermap.org/data/2.5/onecall?lat=47.906&lon=33.395&units=metric&exclude=hourly,daily&appid=c32fd26bff44520278bc12f8b3b65878').json()
    temp = weather['current']['temp']
    wind = weather['current']['wind_speed']
    weath = weather['current']['weather'][0]['description']
    forecast = "Температура: {}\nСкорость ветра: {}\nПогода: {} ".format(temp,wind,weath)
    return forecast

rec_file:str = 'rec.wav'
tgb = bot.TGBotHandler("1141692325:AAGkNyHWLZX7HHqXVu_fpHAWT4jThvxqwbU")
sticker = 'CAACAgIAAxkBAAODX4RsgdDcrnUdFJgj6r4hZqpCaR0AAusBAAIrLT8Z19gEn7d2ETEbBA'
get_weather = {'/weather', '/weather@my_157_test_bot', '/погода', 'погода'}
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
                try:
                    new_file = convert_oga_to_wav(file_from_server)
                    subprocess.run([ffmpeg_path, '-f', 'concat', '-i', 'adding.txt', '-acodec', 'copy', rec_file])
                    text_from_voice = voice_to_text(rec_file)
                    os.remove(file_from_server)
                    os.remove(new_file)
                    os.remove(rec_file)
                    if(text_from_voice.lower() in get_weather):
                        tgb.send_text_message(last_chat_id, get_weather_str())
                    elif(text_from_voice.lower() == 'что ты можешь'):
                        tgb.send_text_message(last_chat_id, 'Могу перевести голосовое сообщение в текст\nА ещё, попробуй сказать \"Погода\"')
                    else:
                        tgb.send_text_message(last_chat_id, "Ваш текст:\n{}".format(text_from_voice))
                except Exception:
                    tgb.send_text_message(last_chat_id, "Извини, я не могу разобрать сказаное :(")
                    os.remove(file_from_server)
                    os.remove(new_file)
                    os.remove(rec_file)
            elif(tgb.get_type_of_message(last_update) == bot.Type_of_message.TEXT):
                if(last_update['message']['text'].lower() in get_weather):
                    tgb.send_text_message(last_chat_id, get_weather_str())
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

