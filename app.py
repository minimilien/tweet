# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 14:52:48 2020

@author: minimilien
"""


from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for,make_response
import webbrowser
from config import Projet,Version
from datetime import datetime
import psutil
from get_tweet import get_20_best



app = Flask(__name__)




@app.route('/')
def index():
    print(request.remote_addr)
    return render_template('index.html',
                        Projet=Projet,
                        Version=Version
                        )



@app.route('/horloge',methods=['GET', 'POST'])
def horloge():
    time=datetime.now()
    return jsonify(result=time.strftime("%H:%M:%S"))


@app.route('/RAM',methods=['GET', 'POST'])
def RAM():
    memoire_utilisee=dict(psutil.virtual_memory()._asdict())['percent']
    return jsonify(result="{}%".format(memoire_utilisee))

@app.route('/sentiments')
def sentiments():
    phrase = request.args.get('phrase', 0, type=str)
    top20="".join(["<p>{}</p>".format(tweet) for tweet in get_20_best(phrase)])
    return jsonify(result=top20,
                   color="#000",
                   )

@app.route('/SIM')
def SIM():
    phrase = "wall"
    top20="".join(["<p>{}</p>".format(tweet) for tweet in get_20_best(phrase)])
    return jsonify(result=top20,
                   color="#000",
                   )



@app.errorhandler(405)
def method_not_allowed(e):
    print(request)
    print(request.remote_addr)
    print(request.form.to_dict())
    return jsonify(result={'info':"Non tu n'as pas le droit."})


@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('index'))


@app.errorhandler(400)
def bad_request(e):
    print(request)
    return jsonify(result={'info':'Non.'})


if __name__ == '__main__':
    #webbrowser.open('http://127.0.0.1:5000/', new=2)
    print("Lancement de l'app")
    app.run(host='0.0.0.0',threaded=True)