from whatsapp import skip, rep, driver, client
import whatsapp
from flask import Flask, render_template
import os
import threading

app = Flask(__name__)

@app.before_first_request
def first():
    t = threading.Thread(target=whatsapp.final_run,args=(skip,rep,driver,client,),daemon=True)
    t.start()

@app.route('/')
def image():
    return '<img src="/static/qr.png">'