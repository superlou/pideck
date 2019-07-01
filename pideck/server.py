#!/usr/bin/env python3
import os
import base64
from os.path import join, isfile
from flask import Flask, flash, request, redirect, url_for
from flask import render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send
from werkzeug.utils import secure_filename
import time
import threading
from .omx import Omx
from .desktop_network_status import show_continuous_status


app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)
socketio = SocketIO(app)


@app.route('/media/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file.save(join(app.config['MEDIA_FOLDER'], filename))
        return redirect('/media')

    return render_template('upload.html')


@app.route('/media')
def media_list():
    media_folder = app.config['MEDIA_FOLDER']
    files = [f for f in os.listdir(media_folder) if isfile(join(media_folder, f))]
    return render_template('media.html', files=files)


@app.route('/player', methods=['GET', 'POST'])
def player():
    if request.method == 'POST':
        if 'play' in request.form:
            filename = request.form['play']
            filepath = join(app.config['MEDIA_FOLDER'], filename)
            app.config['omx'].play(filepath)
        elif 'stop' in request.form:
            app.config['omx'].stop()
        elif 'pause' in request.form:
            app.config['omx'].pause()

    return redirect('/media')


@app.route('/api/player', methods=['GET', 'POST'])
def player_status():
    if request.method == 'GET':
        omx = app.config['omx']
        return jsonify(omx.status())

    if request.method == 'POST':
        for key, val in request.form.items():
            if key == 'action' and val == 'toggle_pause':
                app.config['omx'].pause()
            if key == 'action' and val == 'stop':
                app.config['omx'].stop()
            if key == 'action' and val == 'play':
                source = request.form['source']
                filepath = join(app.config['MEDIA_FOLDER'], source)
                app.config['omx'].play(filepath)
            if key == 'action' and val == 'seek_fraction':
                app.config['omx'].seek_fraction(float(request.form['fraction']))
            if key == 'action' and val == 'set_volume':
                app.config['omx'].set_volume(float(request.form['volume']))                

        return jsonify({'msg': 'ok'})


@app.route('/api/media-files', methods=['GET', 'POST'])
def media_files():
    media_folder = app.config['MEDIA_FOLDER']

    if request.method == 'GET':
        data = [{
            'type': 'media-file',
            'id': base64.b64encode(f.encode()),
            'attributes': {
                'source': f,
            }
        } for i, f in enumerate(os.listdir(media_folder)) if isfile(join(media_folder, f))]

        response = {
            'data': data
        }

        return jsonify(response)

    if request.method == 'POST':
        if 'action' not in request.form:
            return jsonify({'err': 'no action specified'})

        return jsonify({'msg': 'ok'})


@app.route('/api/media-files/<id>', methods=['DELETE', 'OPTIONS'])
def media_file(id):
    media_folder = app.config['MEDIA_FOLDER']

    if request.method == 'OPTIONS':
        return ('', 204)

    if request.method == 'DELETE':
        filename = base64.b64decode(id).decode()
        filepath = join(media_folder, filename)
        print(filepath)

        if not isfile(filepath):
            return jsonify({'err': 'file not found'})

        os.remove(filepath)
        return ('', 204)

    return jsonify({'msg': 'ok'})


@app.route('/api/media-files/upload', methods=['POST', 'OPTIONS'])
def media_file_upload():
    if request.method == 'OPTIONS':
        return ('', 204)

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'err': 'no file part'});

        file = request.files['file']

        if file.filename == '':
            return jsonify({'err': 'no selected file'});

        filename = secure_filename(file.filename)
        file.save(join(app.config['MEDIA_FOLDER'], filename))
        return jsonify({'msg': 'ok'});


@app.before_first_request
def start_send_player_status():
    t = threading.Thread(target=send_player_status, args=(app.config['omx'], ))
    t.daemon = True
    t.start()


def send_player_status(omx):
    while (1):
        try:
            socketio.send({'player_status': omx.status()})
        except Exception:
            pass

        time.sleep(0.02)


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def main():
    show_continuous_status(5)

    app.config['MEDIA_FOLDER'] = 'media'
    create_folder(app.config['MEDIA_FOLDER'])
    app.config['omx'] = Omx(app.config['MEDIA_FOLDER'])
    app.config['DEBUG'] = True

    socketio.run(app, host='0.0.0.0', port=8910, debug=True)


if __name__ == '__main__':
    main()
