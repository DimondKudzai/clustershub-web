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

clusters = get_all_clusters()

@app.route("/groupChat/<int:cluster_id>")
def group_chat(cluster_id):
    cluster = next((c for c in clusters if c['id'] == cluster_id), None)
    if not cluster:
        return "Cluster not found", 404
    return render_template("conversations.html", cluster=cluster)

@app.route("/api/groupChat/<int:cluster_id>/threads", methods=["GET"])
def api_get_threads(cluster_id):
    cluster = next((c for c in clusters if c['id'] == cluster_id), None)
    if not cluster:
        return jsonify({"error": "Cluster not found"}), 404
    return jsonify(cluster.get("conversations", []))

@app.route("/api/groupChat/<int:cluster_id>/threads", methods=["POST"])
def api_add_thread(cluster_id):
    data = request.get_json()
    title = data.get("title", "").strip()
    body = data.get("body", "").strip()
    if not title or not body:
        return jsonify({"error": "Title and body required"}), 400

    cluster = next((c for c in clusters if c['id'] == cluster_id), None)
    if not cluster:
        return jsonify({"error": "Cluster not found"}), 404

    new_thread = {"chatId": len(cluster["conversations"])+1,
                  "title": title,
                  "author": data.get("author", "Anonymous"),
                  "comments": []}
    cluster["conversations"].append(new_thread)
    return jsonify(new_thread), 201

@app.route("/api/groupChat/<int:cluster_id>/threads/<int:thread_index>/comments", methods=["POST"])
def api_add_comment(cluster_id, thread_index):
    data = request.get_json()
    text = data.get("text", "").trim()
    if not text:
        return jsonify({"error": "Comment text required"}), 400

    cluster = next((c for c in clusters if c['id'] == cluster_id), None)
    if not cluster or thread_index < 0 or thread_index >= len(cluster["conversations"]):
        return jsonify({"error": "Not found"}), 404

    comment = {"user": data.get("user", "Anonymous"),
               "text": text,
               "timestamp": data.get("timestamp")}
    cluster["conversations"][thread_index]["comments"].append(comment)
    return jsonify(comment), 201


if __name__ == '__main__':
    app.run(debug=True)
