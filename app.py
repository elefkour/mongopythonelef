from flask import Flask, jsonify
from flask import Flask, redirect
from flask import request
from flask import render_template
import html
import json
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["song_db"]
    return db

@app.route('/')
def ping_server():
    return render_template('index.html')

@app.route('/songs')
def get_stored_songs():
    db=""
    try:
        db = get_db()
        _songs = db.song_tb.find()
        songs = [{"id": song["id"], "name": song["name"],"artist": song["artist"], "type": song["type"]} for song in _songs]
        return render_template('songs.html', title="page", jsonfile=json.dumps(songs))
    except:
        pass
    finally:
        if type(db)==MongoClient:
            db.close()
@app.route('/create', methods=('GET', 'POST'))
def create():
    data = {}
    if request.method == 'POST':
        data['id'] = request.form['id']
        data['name'] = request.form['name']
        data['artist'] = request.form['artist']
        data['type'] = request.form['type']
        db=""
        try:
            db = get_db()
            songs = db.song_tb.insert_one(data)
            return redirect("http://localhost:5000/songs")
        except:
            pass

        finally:
            if type(db)==MongoClient:
                db.close()

    return render_template('create.html')

@app.route("/add_one")
def add_songs():
    db=""
    try:
        db = get_db()
        songs = db.song_tb.insert_one({"id":"4", "name":"never","artist": "BTS", "type": "rock"})
        return redirect("http://localhost:5000/songs")

    except:
        pass
    finally:
        if type(db)==MongoClient:
            db.close()

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)