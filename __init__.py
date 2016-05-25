import os, datetime, time
import path
import shutil
import re
import subprocess

from os import walk

from path import path
from flask import Flask, url_for, request, redirect, render_template

# Change asterisk extensions.conf to to the hosted route. 


# Change to actual directory
UPLOAD_FOLDER = '/home/kasadaka/KasaDaka/FlaskKasadaka/FlaskKasadaka/static/messages'
ALLOWED_EXTENSIONS = set(['wav'])

messages_dir = '/home/kasadaka/KasaDaka/FlaskKasadaka/FlaskKasadaka/static/messages'

# Create an instance of the Flask Class
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Utility to check received messages are in the correct format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/voice')
def index():
    #Change the DAYS based on farmer feedback
    DAYS = 5
    removed = 0
    d = path(messages_dir)
    print(d)
    time_in_secs = time.time() - (DAYS * 24 * 60 * 60)
   
    # For each file in messages directory check if it should be removed
    for i in d.walk():
        #print(time.ctime(os.path.getmtime(i)))
        if i.isfile():
            # If file is older than DAYS, remove it
            if i.mtime <= time_in_secs:
                i.remove()
                removed += 1
    print(removed)
    return render_template("main.vxml")


@app.route('/voice/<language>')
def get_messages(language):
    language_send = str(language)
    language_code = language_send[0:2]
    message_files = [f for f in os.listdir(messages_dir) if f.endswith('wav')]
    language_files = [f for f in message_files if (f.startswith(str(language)) and "coop" not in f)]
    coop_messages = [f for f in language_files if "coop" in f]
    message_files_number = len(language_files)
    coop_messages_number = len(coop_messages)
    return render_template("new_options_menu.vxml", message_files_number = message_files_number,
                        message_files = language_files, language = language_send, 
                        language_code = language_code, coop_messages = coop_messages,
                        coop_messages_number = coop_messages_number)
                        
# Receive recordings, save them with appropriate name, and render xml
@app.route('/voice/recording/<language>', methods=['GET', 'POST'])
def upload_file(language):
    #print request.form
    file_path = request.form['record']
    saveRecording(file_path)
    # print(file_path)
    #file_path_correct = '"' + file_path +'"'
    file_path_correct = str(file_path)
    language_send = str(language)
    language_code = language_send[0:2]
    #print(language_send, language_code)
    print(file_path_correct)
    print(len(file_path_correct))
    print(type(file_path_correct))
    short_path = file_path_correct[25:]
    print(short_path)
    shutil.move(short_path, messages_dir)

    if request.method == 'POST':
        file = request.files['message']
        if file and allowed_file(file.filename):
            filename = str(language)+"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".wav"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('recording_received.vxml', language_code = language_code)
    return render_template('not_recorded.vxml', language_code = language_code)

# Receive Coop Recordings and save them. 
@app.route('/voice/recording/coop/<language>', methods=['GET', 'POST'])
def upload_coop_file(language):
    language_send = str(language)
    language_code = language_send[0:2]
    if request.method == 'POST':
        file = request.files['message']
        if file and allowed_file(file.filename):
            filename = str(language)+"_"+"coop_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".wav"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('recording_received.vxml', language_code = language_code)
    return render_template('not_recorded.vxml', language_code = language_code)


# Section for viewing and playing all audio files 
@app.route('/')
def overview():
    music_files = [f for f in os.listdir(messages_dir) if f.endswith('wav')]
    music_files_number = len(music_files)
    return render_template("index.html",
                        title = 'Home',
                        music_files_number = music_files_number,
                        music_files = music_files)

@app.route('/<filename>')
def song(filename):
    return render_template('play.html',
                        title = filename,
                        music_file = filename)

def saveRecording(path):
    #remove file:// if present
    #a lot of %00 stuff to remove
    path =  path.replace("\00","")
    path = re.sub(r"(file:\/\/)?(.*)",r"\2",path)
    #dest = findFreshFilePath(messages_dir+ "recording.wav")
    dest = messages_dir
    print(path)
    print(dest)
    #convert to format that is good for vxml as well as web interface
    #subprocess.call(['/usr/bin/sox',path,'-r','8k','-c','1','-e','signed-integer',dest])
    shutil.copy(path,dest)
    return dest

def findFreshFilePath(preferredPath):
    addition = 1
    path = re.sub(r"(.*\/)(\w*)(\.\w{3})",r"\1\2" + "_" + str(addition) + r"\3",preferredPath)
    while os.path.isfile(path):
        addition = addition + 1
        path = re.sub(r"(.*\/)(\w*)(\.\w{3})",r"\1\2" + "_" + str(addition) + r"\3",preferredPath)
    return path





# if run from the terminal, define cloud9 host and port
if __name__ == '__main__':
    # Below items are not needed if running on a linux machine, just for Cloud9
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True
    app.run(host=host, port=port)

 