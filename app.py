from flask import Flask, jsonify, request, send_file, redirect
import sqlite3
import datetime
import os
from werkzeug.utils import secure_filename
import urllib.request
import json
from math import trunc

app = Flask(__name__)

#con = sqlite3.connect('metadata.db')

@app.route('/')
def index():
    return "Hello World"

@app.route('/test/')
def test():
    con = sqlite3.connect('metadata.db')
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES ('user1', 'supercomputer', 2, 15)")
    con.commit()
    con.close()
    user = {'id': 'user1'}
    return jsonify(user)

@app.route('/register/', methods=['POST'])
def register():
    print(request.data)
    print(request.json['minutes'])
    con = sqlite3.connect('metadata.db')
    cur = con.cursor()
    cur.execute("INSERT INTO USERS ('SPEC','MINUTES','STATUS','IP') VALUES ('" + request.json['spec']+"', "+request.json['minutes']+", 'READY', '"+request.json['IP']+ "')")
    user_id = cur.lastrowid
    con.commit()
    con.close()
    return str(user_id)

@app.route('/up/<int:user_id>')
def up(user_id):
    con = sqlite3.connect('metadata.db')
    cur = con.cursor()
    cur.execute("UPDATE USERS SET TIMESTAMP = datetime('now','localtime'), MINUTES = MINUTES-1"+" WHERE USER_ID ="+str(user_id))
    (status, master_ip, world_size, job_id, rank) = cur.execute("SELECT STATUS, MASTER_IP, WORLD_SIZE, JOB_ID, RANK FROM USERS WHERE USER_ID ="+str(user_id)).fetchall()[0]
    #tstamp = {'timestamp': datetime.datetime.now()}
    #print(status)
    con.commit()
    con.close()
    response = {'status': status, 'master_ip': master_ip, 'world_size': world_size, 'job_id': job_id, 'rank': rank}
    return jsonify(response)

@app.route('/downloads/')
def return_files():
    try:
        return send_file('/users/tkhan27/dist_project/file_store/test.zip', download_name ='dist_training.zip')
    except Exception as e:
        return str(e)

ALLOWED_EXTENSIONS = set(['zip'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/registerJob/', methods=['POST'])
def register_job():
    #ALLOWED_EXTENSIONS = set(['zip'])
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    data=json.loads(request.form.get('data'))
    con = sqlite3.connect('metadata.db')
    cur = con.cursor()
    #assign credits for now 100
    cur.execute("INSERT INTO JOBS ('CREDITS','JOB_DURATION','NODES','STATUS') VALUES (100, "+ data['job_duration']+", "+data['nodes']+", 'READY')")
    job_id = cur.lastrowid
    con.commit()
    con.close()
    print(data)
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        directory = os.path.join(os.getcwd()+"/file_store/", "jobid"+str(job_id))
        if not os.path.exists(directory):
                os.makedirs(directory)
        file.save(os.path.join(directory, filename))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are zip'})
        resp.status_code = 400
        return resp

if __name__ == "__main__":
    app.run(threaded=True, debug=True)
