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
        location=user.get('location', ''),
        email=user['email'],
        website=user['website'],
        skillA=user['skills'][0],
        skillB=user['skills'][1],
        skillC=user['skills'][2]
    )

@app.route('/login')
def login():
    return render_template('auth.html')

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
	    location=user.get('location', ''), 
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

@app.route('/clusters/chat/<int:cluster_id>')
def show_cluster(cluster_id):
    cluster = next((c for c in clusters if c['id'] == cluster_id), None)
    if not cluster:
        return "Cluster not found", 404
    return render_template('conversations.html', cluster=cluster)
    
@app.route('/clusters/<int:cluster_id>/threads/<int:thread_id>/comments', methods=['POST'])
def post_comment(cluster_id, thread_id):
    user = request.form['user']
    text = request.form['text']
    timestamp = datetime.utcnow().isoformat()

    cluster = next((c for c in clusters if c['id'] == cluster_id), None)
    if not cluster:
        return "Cluster not found", 404

    thread = next((t for t in cluster['conversations'] if t['chatId'] == thread_id), None)
    if not thread:
        return "Thread not found", 404

    thread['comments'].append({
        "user": user,
        "text": text,
        "timestamp": timestamp
    })

    return redirect(url_for('show_cluster', cluster_id=cluster_id))

@app.route('/recommended_clusters')
def recommended_clusters():
    clusters = get_all_clusters()
    users = get_all_users()
    if not users:
        return "No users found", 404
    current_user = users[0]  # simulate logged-in user
    user_skills = set(current_user.get('skills', []))

    # Score clusters based on skill/tag match
    scored = []
    for cluster in clusters:
        tags = set(cluster.get('tags', []))
        match_count = len(user_skills & tags)
        scored.append((match_count, cluster))

    # Sort clusters by best match
    scored.sort(key=lambda x: x[0], reverse=True)

    # First: 3/3, 2/3, 1/3 matches
    matched_clusters = [c for score, c in scored if score > 0]

    # Second: target match if no tag matches
    if not matched_clusters:
        matched_clusters = [
            c for c in clusters 
            if any(skill.lower() in c.get('target', '').lower() for skill in user_skills)
        ]

    # Third: word match between skills and target
    if not matched_clusters:
        target_scored = []
        for cluster in clusters:
            target_words = cluster.get('target', '').lower().split()
            skill_matches = sum(1 for skill in user_skills if any(skill.lower() in target_word for target_word in target_words))
            target_scored.append((skill_matches, cluster))
        target_scored.sort(key=lambda x: x[0], reverse=True)
        matched_clusters = [c for score, c in target_scored if score > 0]

    # Fourth: fallback to clusters with most members
    if not matched_clusters:
        matched_clusters = sorted(clusters, key=lambda x: len(x.get('members', [])), reverse=True)

    return render_template('recommended.html', clusters=matched_clusters, user=current_user)
    

if __name__ == '__main__':
    app.run(debug=True)
