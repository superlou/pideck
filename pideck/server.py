#!/usr/bin/env python3
import os
from os.path import join, isfile
from flask import Flask, flash, request, redirect, url_for
from flask import render_template
from werkzeug.utils import secure_filename
from omxplayer.player import OMXPlayer


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
            player = OMXPlayer(filepath)

    return redirect('/media')


def main():
    app.config['MEDIA_FOLDER'] = 'media'
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=8910)


if __name__ == '__main__':
    main()
