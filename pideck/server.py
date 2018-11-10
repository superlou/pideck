#!/usr/bin/env python3
import os
from os.path import join, isfile
from flask import Flask, flash, request, redirect, url_for
from flask import render_template, jsonify
from werkzeug.utils import secure_filename
from .omx import Omx


app = Flask(__name__)
app.secret_key = os.urandom(24)


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


@app.route('/player.json')
def player_status():
    omx = app.config['omx']
    return jsonify(omx.status())


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def main():
    app.config['MEDIA_FOLDER'] = 'media'
    create_folder(app.config['MEDIA_FOLDER'])
    app.config['omx'] = Omx()
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=8910)


if __name__ == '__main__':
    main()
