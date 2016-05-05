import os, datetime, time
import path

from os import walk

from path import path
from flask import Flask, url_for, request, redirect, render_template


# Create Setup section and reuse the variables on all other pages
# Make for easy setup on a new system

UPLOAD_FOLDER = '/home/ubuntu/workspace/flask_init/static/messages'
ALLOWED_EXTENSIONS = set(['wav'])

messages_dir = '/home/ubuntu/workspace/flask_init/static/messages'

# Create an instance of the Flask Class
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Utility to check received messages are in the correct format
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/voice')
@app.route('/home')
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
    return render_template("main.xml")

@app.route('/voice/<language>')
def get_messages(language):
    language_send = str(language)
    language_code = language_send[0:2]
    message_files = [f for f in os.listdir(messages_dir) if f.endswith('wav')]
    language_files = [f for f in message_files if (f.startswith(str(language)) and "coop" not in f)]
    coop_messages = [f for f in language_files if "coop" in f]
    message_files_number = len(language_files)
    coop_messages_number = len(coop_messages)
    return render_template("options_menu.xml", message_files_number = message_files_number,
                        message_files = language_files, language = language_send, 
                        language_code = language_code, coop_messages = coop_messages,
                        coop_messages_number = coop_messages_number)
                        
# Receive recordings, save them with appropriate name, and render xml
@app.route('/voice/recording/<language>', methods=['GET', 'POST'])
def upload_file(language):
    language_send = str(language)
    language_code = language_send[0:2]
    if request.method == 'POST':
        file = request.files['message']
        if file and allowed_file(file.filename):
            filename = str(language)+"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M")+".wav"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('recording_received.xml', language_code = language_code)
    return render_template('not_recorded.xml', language_code = language_code)

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
            return render_template('recording_received.xml', language_code = language_code)
    return render_template('not_recorded.xml', language_code = language_code)




# if run from the terminal, define cloud9 host and port
if __name__ == '__main__':
    # Below items are not needed if running on a linux machine, just for Cloud9
    host = os.getenv('IP', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    app.debug = True
    app.run(host=host, port=port)

 