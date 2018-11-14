#!/usr/bin/env python3
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="pideck",
    version="0.1.0",
    author="Louis Simons",
    author_email="lousimons@gmail.com",
    description="Raspberry Pi Playback Deck",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        'flask',
        'omxplayer-wrapper',
        'werkzeug',
        'flask-cors',
        'flask-socketio',
        'gevent',		# eventlet didn't work with ember-websockets
        'gevent-websocket',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Raspbian",
    ],
    entry_points={
        'console_scripts': [
            'pideck=pideck.server:main'
        ]
    }
)
