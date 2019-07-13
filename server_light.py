#!/usr/bin/env python3
import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, send
from display import set_display_mode
import threading
import time


app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)
socketio = SocketIO(app)


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['MEDIA_FOLDER'] = 'media'
create_folder(app.config['MEDIA_FOLDER'])
app.config['DEBUG'] = True

from omxplayer.player import OMXPlayer
@app.route('/')
def index():
    OMXPlayer('media/VIDDYOZE-Logo_pop.mp4')
    return jsonify({'msg': 'ok'})


from threading import Lock
thread = None
thread_lock = Lock()


def send_player_status():
    while True:
        socketio.sleep(0.1)
        try:
            msg = {'msg': 'simple_response'}
            socketio.emit('custom', msg)
        except Exception as e:
            print(e)


@socketio.on('message')
def handle_message(msg):
    socketio.send({'msg': 'here'})


@socketio.on('connect')
def handle_connect():
    global thread
    socketio.send({'msg': 'here connect'})
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(send_player_status)



def main():
    socketio.run(app, host='0.0.0.0', port=8910)


if __name__ == '__main__':
    main()
