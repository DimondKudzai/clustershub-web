from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os

from datetime import datetime
from flask import jsonify
#from services.appData import get_all_users, get_all_clusters, get_suggestions
from models import db
from config import Config
from models import User, Cluster, Suggestion # Import models

import sqlite3


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()  # Create tables


@app.route('/')
def index():
    users = User.query.all()
    user = users[0]
    return render_template(
        'dashboard.html',
        name=user.name,
        clustersCount=user.clusters_count,
        notificationsCount=user.notifications_count
    )
@app.route('/home')
def home():
    users = User.query.all()
    user = users[1]
    created_clusters = user.get_created_clusters()
    cluster_count = len(created_clusters)
    messages = user.get_messages()
    
    # Count unread
    unread_count = sum(1 for m in messages if not m.get("read", False))
    
    return render_template(
        'dashboard.html',
        name=user.name,
        clustersCount=cluster_count,
        notificationsCount=unread_count
    )
    
@app.route('/startCluster')
def startCluster():
    suggested = get_suggestions()
    return render_template('createCluster.html', suggested_skills=suggested)

@app.route('/myProfile')
def myProfile():
    users = get_all_users()
    if users:
        user = users[0]
        return render_template('profile.html', user=user)
    else:
        # Handle the case where no users are found
        return 'No users found', 404
        
@app.route('/login')
def login():
    return render_template('auth.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/users")
def users():
    return jsonify(get_all_users())
    
@app.route("/users/<name>")
def getUser(name):
	users = get_all_users()
	user = next((u for u in users if str(u['name']) == str(name)), None)
	if user:
   	    return render_template('profile.html', user=user)
	else:
	# Handle the case where no users are found
	    return 'No users found', 404
	    
# Clusters
	    
@app.route('/clusters')
def clusters():
    user = get_all_users()[0]
    clusters = get_all_clusters()
    
    created_clusters = user.get("created_clusters", [])
    requested_ids = user.get("clusters_requests", [])

    total_clusters = created_clusters + requested_ids 
    cluster_count = len(total_clusters)

    requested_clusters = [c for c in clusters if c['id'] in total_clusters]

    if requested_clusters:
        return render_template(
            'clusters.html',
            user=user,
            clusters=requested_clusters,
            clustersCount=cluster_count
        )
    return "no clusters", 404


@app.route("/clusters/<int:id>")
def getCluster(id):
    user = get_all_users()[0]
    clusters = get_all_clusters()
    cluster = next((c for c in clusters if c['id'] == id), None)

    if cluster:
        return render_template("cluster_detail.html", cluster=cluster)

    return jsonify({'error': 'Cluster not found'}), 404
        
# Notifications        
        
@app.route("/notifications")
def notifications():
    user = get_all_users()[1]
    messages = user.get("messages", [])
    return render_template("notifications.html", messages=messages)



@app.route("/notifications/read/<int:msg_id>")
def mark_read(msg_id):
    user = get_all_users()[0]
    for msg in user.get("messages", []):
        if msg.get("id") == msg_id:
            msg["read"] = True
    return redirect(url_for("notifications"))

# Requests

@app.route('/clusters/requests/<int:cluster_id>')
def requested(cluster_id):
    clusters = get_all_clusters()
    user = get_all_users()[0]
    cluster = next((c for c in clusters if c['id'] == cluster_id), None)
    if not cluster:
        return "Cluster not found", 404
    return render_template('requests.html', cluster=cluster)
   
@app.route('/user_requests')
def user_requests():
    clusters = get_all_clusters()
    users = get_all_users()
    user = users[0]  # simulate logged-in user
    requested_ids = user.get("clusters_requests", [])
    requested_count = len(requested_ids)
    requested_clusters = [c for c in clusters if c['id'] in requested_ids]
    
    if requested_clusters:
        return render_template('user_request.html', user=user, cluster=requested_clusters, clustersCount=requested_count)
    return "no requests",404


@app.route('/send_cluster_request', methods=['POST'])
def send_cluster_request():
    user = get_all_users()[0]  # Simulate logged-in user
    cluster_id = int(request.form['cluster_id'])
    message = request.form['message']

    cluster = next((c for c in get_all_clusters() if c['id'] == cluster_id), None)
    if not cluster:
        return "Cluster not found", 404

    request_obj = {
        "author": user["name"],
        "title": "Join Request",
        "body": message,
        "created": datetime.utcnow().isoformat(),
        "comments": []
    }

    if "requests" not in cluster:
        cluster["requests"] = []
    cluster["requests"].append(request_obj)

    return redirect(url_for('requested', cluster_id=cluster_id))

#clusters

@app.route('/clusters/chat/<int:cluster_id>')
def show_cluster(cluster_id):
    clusters = get_all_clusters()
    user = get_all_users()[0]
    cluster = next((c for c in clusters if c['id'] == cluster_id), None)
    if not cluster:
        return "Cluster not found", 404
    return render_template('conversations.html', cluster=cluster)
    
@app.route('/clusters/<int:cluster_id>/threads/<int:thread_id>/comments', methods=['POST'])
def post_comment(cluster_id, thread_id):
    clusters = get_all_clusters()
    user = get_all_users()[0]
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

# App Algo

@app.route('/recommended_clusters')
def recommended_clusters():
    clusters = get_all_clusters()
    users = get_all_users()
    if not users:
        return "No users found", 404
    
    current_user = users[0]
    user_skills = set(current_user.get('skills', []))
    user_desc_words = set(current_user.get('description', '').lower().split())
    
    scored = []
    for cluster in clusters:
	    score = 0
	    
	 
	  # compare tags
	    user_skills_lower = set(skill.lower() for skill in user_skills)
	    tags_lower = set(tag.lower() for tag in cluster.get('tags', []))
	  
  	  # Tag match scoring
	    score += 3 * len(user_skills_lower & tags_lower)

	    
	    # Skill in target string
	    if any(skill.lower() in cluster.get('target', '').lower() for skill in user_skills):
	        score += 2
	    
	    # Word match between skills and target
	    target_words = cluster.get('target', '').lower().split()
	    skill_matches = sum(1 for skill in user_skills if any(skill.lower() in word for word in target_words))
	    score += skill_matches
	    
	    # Match user description with target
	    desc_matches = sum(1 for word in user_desc_words if word in target_words)
	    score += desc_matches
	    
	    # Fallback: more members = better
	    score += 0.1 * len(cluster.get('members', []))
	    
	    scored.append((score, cluster))
    
    #Sort by final score (descending)
    scored.sort(key=lambda x: x[0], reverse=True)
    matched_clusters = [c for score, c in scored if score > 0]
    
    return render_template('recommended.html', clusters=matched_clusters, user=current_user)
    
    
#simple endpoints

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')
    
@app.route('/logout')
def logout():
    #session.clear()
    return redirect('/login')


#settings
@app.route('/profile_settings')
def profile_settings():
    return render_template('set_profile.html')

@app.route('/cluster_settings')
def cluster_settings():
    return render_template('cluster_settings.html')
    
    
if __name__ == '__main__':
    app.run(debug=True)