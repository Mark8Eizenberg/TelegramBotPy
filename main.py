import subprocess

 #convert oga to ogg
def convert_oga_to_ogg(file_path):
    end_file = 'temp.ogg'
    subprocess.run(['ffmpeg', '-i', file_path, end_file])
    return None

