from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import jsonify
from services.appData import get_all_users

app = Flask(__name__)

@app.route('/')
def index():
    name = get_all_users()[0]['name']
    return render_template('dashboard.html',name=name)

@app.route('/home')
def home():
    name = get_all_users()[0]['name']
    return render_template('dashboard.html',name=name)
        
    
@app.route('/startCluster')
def startCluster():
    return render_template('createCluster.html')

@app.route('/myProfile')
def myProfile():
    name = get_all_users()[0]['name']
    description = get_all_users()[0]['description']
    email = get_all_users()[0]['email']
    website = get_all_users()[0]['website']
    return render_template('profile.html',name=name,description=description,email=email,website=website)

@app.route('/login')
def login():
    return render_template('profile.html')

@app.route('/groupChat')
def groupChat():
    return render_template('conversations.html')

@app.route("/users")
def users():
    return jsonify(get_all_users())
    
if __name__ == '__main__':
    app.run(debug=True)