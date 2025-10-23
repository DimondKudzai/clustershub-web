from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import sqlite3
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import jsonify
from services.appData import get_all_users, get_all_clusters

app = Flask(__name__)

@app.route('/')
def index():
    user = get_all_users()[4]
    return render_template(
        'dashboard.html',
        name=user['name'],
        clustersCount=user['clustersCount'],
        notificationsCount=user['notificationsCount']
    )
@app.route('/home')
def home():
    user = get_all_users()[2]
    return render_template(
        'dashboard.html',
        name=user['name'],
        clustersCount=user['clustersCount'],
        notificationsCount=user['notificationsCount']
    )
@app.route('/startCluster')
def startCluster():
    return render_template('createCluster.html')

@app.route('/myProfile')
def myProfile():
    user = get_all_users()[0]
    return render_template(
        'profile.html',
        name=user['name'],
        description=user['description'],
        email=user['email'],
        website=user['website'],
        skillA=user['skills'][0],
        skillB=user['skills'][1],
        skillC=user['skills'][2]
    )

@app.route('/login')
def login():
    return render_template('profile.html')

@app.route('/groupChat')
def groupChat():
    return render_template('conversations.html')

@app.route("/users")
def users():
    return jsonify(get_all_users())
    
@app.route("/users/<name>")
def getUser(name):
	users = get_all_users()
	user = next((u for u in users if u['name'] == name), None)
	if user:
		return render_template(
		'profile.html', 
		name=user['name'], 
		description=user.get('description', ''), 
		email=user.get('email', ''), 
		website=user.get('website', ''),
		skillA=user['skills'][0],
		skillB=user['skills'][1],
		skillC=user['skills'][2]
		)
	return jsonify({'error': 'User not found'}), 404

@app.route('/clusters')
def clusters():
    cluster = get_all_clusters()
    user = get_all_users()[0]
    return render_template(
        'clusters.html',
        clustersCount=user['clustersCount'],
        clusters=cluster,
        name=user['name'],
        id=user['id']
    )
   
@app.route("/clusters/<int:id>")
def getCluster(id):
    user = get_all_users()[0]
    clusters = get_all_clusters()
    cluster = next((c for c in clusters if c['id'] == id), None)

    if cluster:
        return render_template("cluster_detail.html", cluster=cluster)

    return jsonify({'error': 'Cluster not found'}), 404
        
@app.route("/notifications")
def notifications():
    user = get_all_users()[0]
    messages = user["messages"]
    #message = next((m for m in messages if m['id'] == id), None)
    return render_template("notifications.html", messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
