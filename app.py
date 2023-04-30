import os
import sys
from flask import Flask
import pymongo

STATIC_FOLDER = sys.path[0] + '/static/'
TEMPLATES_FOLDER = sys.path[0] + '/templates/'
app = Flask(__name__, template_folder=TEMPLATES_FOLDER, static_folder=STATIC_FOLDER)

app.config['MONGO_URI'] = 'mongodb+srv://priyankakannan:ammu0229@cluster0.h1g8883.mongodb.net/?retryWrites=true&w=majority'
app.secret_key = "SSKEY"

client = pymongo.MongoClient("mongodb+srv://priyankakannan:ammu0229@cluster0.h1g8883.mongodb.net/?retryWrites=true&w=majority")
db = client.complaint