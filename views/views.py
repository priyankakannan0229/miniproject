from flask import make_response,Flask, flash, redirect, render_template, request, url_for, session
from app import *

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')