#!/usr/bin/env python
from flask import render_template, request, Flask, flash, redirect
from app import app
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import requests, time, json, os
from time import sleep

hostip = '192.168.1.139'
url = 'http://'+hostip+':35747/'

history = []

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

def getSong():
    r = requests.get(url + 'currentsong')
# check for malformed json
    try:
        x = r.json()
# if malformed, split the last section
    except:
        djson = r.content.decode('utf-8').split(',"IsStillValid"',1)[0]
        x = json.loads(djson + '}')

    artist = x['Artist']
    title = x['SongTitle']
    audioURL = x['AudioUrl']
    imgURL = x['AlbumArtUrl']
    loved = x['Loved']

    if title not in str(history):
        history.append({'artist':artist, 'title':title, 'imgURL':imgURL, 'loved':loved})
    if len(history) > 7:
        history.pop(0)
    
    return {
            'artist':artist,
            'title':title,
            'audioURL':audioURL,
            'imgURL':imgURL,
            'loved': loved
            }

def dislikeSong():
    r = requests.get(url + 'dislike')
    sleep(1)
    flash('Disliked', 'danger')
    return redirect('/index')

def nextSong():
    r = requests.get(url + 'next')
    sleep(1)
    flash('Next', 'info')
    return redirect('/index')

def likeSong():
    r = requests.get(url + 'like')
    flash('Liked', 'success')
    sleep(1)
    return redirect('/index')

def playSong():
    r = requests.get(url + 'toggleplaypause')
    sleep(1)
    flash('Pause', 'info')
    return redirect('/index')

@app.route('/', methods=['GET','POST'])
@app.route('/index')

def index():
    form = ReusableForm(request.form)
    print(form.errors)

    if request.method == 'POST':
        if request.form['btn'] == 'next':
            nextSong()
        elif request.form['btn'] == 'dislike':
            dislikeSong()
        elif request.form['btn'] == 'like':
            likeSong()
        elif request.form['btn'] == 'play':
            playSong()

    songTitle = getSong()['title']
    artist = getSong()['artist']
    imgURL = getSong()['imgURL']
    loved = getSong()['loved']

    return render_template('index.html',
            form=form,
            title='Elpis Remote',
            songTitle=songTitle,
            artist=artist,
            imgURL=imgURL,
            loved=loved,
            history=history 
            )

