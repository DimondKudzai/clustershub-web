from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session
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
app.config['SECRET_KEY'] = '24091996'


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
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    created_clusters = user.get_created_clusters()
    cluster_count = len(created_clusters)
    messages = user.get_messages()
    # Count unread
    unread_count = sum(1 for m in messages if not m.get("read", False))
    return render_template('dashboard.html', name=user.name, clustersCount=cluster_count, notificationsCount=unread_count)
    
    
@app.route('/startCluster')
def startCluster():
    suggested = Suggestion.query.first()
    if suggested:
        suggested_skills = suggested.get_skills()
    else:
        suggested_skills = []
    return render_template('createCluster.html', suggested_skills=suggested_skills)
    
    
@app.route('/myProfile')
def myProfile():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    return render_template('profile.html', user=user)
        
@app.route('/login')
def login():
    return render_template('auth.html')


@app.route('/login_handler', methods=['POST'])
def login_handler():
    try:
        username = request.form['username'].strip()
        password = request.form['password'].strip()
    except KeyError:
        return redirect('/login')

    users = User.query.all()
    user = next((u for u in users if (u.name.strip().lower() == username.lower() or u.email.strip().lower() == username.lower()) and u.password == password), None)
    if user:
        session['user_id'] = user.id
        return redirect('/home')
    else:
        return redirect('/login')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route("/users")
def users():
    return jsonify(User.query.all())
    
@app.route("/users/<name>")
def getUser(name):
	users = User.query.all()
	user = next((u for u in users if str(u.name) == str(name)), None)
	if user:
   	    return render_template('profile.html', user=user)
	else:
	# Handle the case where no users are found
	    return 'No users found', 404
	    
# Clusters
	    
@app.route('/clusters')
def clusters():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    clusters = Cluster.query.all()
    created_clusters = user.get_created_clusters()
    requested_clusters = user.get_clusters_requests()
    total_clusters = created_clusters + requested_clusters
    cluster_count = len(total_clusters)
    requested_clusters = [c for c in clusters if c.id in total_clusters]
    if requested_clusters:
        return render_template('clusters.html', user=user, clusters=requested_clusters, clustersCount=cluster_count)
    return "no clusters", 404

@app.route("/clusters/<int:id>")
def getCluster(id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    cluster = Cluster.query.get(id)
    if cluster:
        return render_template("cluster_detail.html", cluster=cluster)
    return jsonify({'error': 'Cluster not found'}), 404
        
# Notifications        
        
@app.route("/notifications")
def notifications():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    messages = user.get_messages()
    return render_template("notifications.html", messages=messages)
    


@app.route("/notifications/read/<int:msg_id>")
def mark_read(msg_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    messages = user.get_messages()
    for msg in messages:
        if msg.get("id") == msg_id:
            msg["read"] = True
    user.set_messages(messages)
    db.session.commit()
    return redirect(url_for("notifications"))



# Requests

@app.route('/clusters/requests/<int:cluster_id>')
def requested(cluster_id):
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        return "Cluster not found", 404
    return render_template('requests.html', cluster=cluster)
   
   
@app.route('/user_requests')
def user_requests():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    clusters = Cluster.query.all()
    requested_ids = user.get_clusters_requests()
    requested_count = len(requested_ids)
    requested_clusters = [c for c in clusters if c.id in requested_ids]
    if requested_clusters:
        return render_template('user_request.html', user=user, clusters=requested_clusters, clustersCount=requested_count)
    return "no requests", 404

@app.route('/send_cluster_request', methods=['POST'])
def send_cluster_request():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    cluster_id = int(request.form['cluster_id'])
    message = request.form['message']
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        return "Cluster not found", 404

    requests = cluster.get_requests()
    request_obj = {
        "author": user.name,
        "title": "Join Request",
        "body": message,
        "created": datetime.utcnow().isoformat(),
        "comments": []
    }
    requests.append(request_obj)
    cluster.set_requests(_requests)
    db.session.commit()
    return redirect(url_for('requested', cluster_id=cluster_id))

#clusters

@app.route('/clusters/chat/<int:cluster_id>')
def show_cluster(cluster_id):
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        return "Cluster not found", 404
    return render_template('conversations.html', cluster=cluster)
    
@app.route('/clusters/<int:cluster_id>/threads/<int:thread_id>/comments', methods=['POST'])
def post_comment(cluster_id, thread_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        return "Cluster not found", 404

    conversations = cluster.get_conversations()
    thread = next((t for t in conversations if t['chatId'] == thread_id), None)
    if not thread:
        return "Thread not found", 404

    text = request.form['text']
    timestamp = datetime.utcnow().isoformat()
    thread['comments'].append({
        "user": user.name,
        "text": text,
        "timestamp": timestamp
    })
    cluster.set_conversations(conversations)
    db.session.commit()
    return redirect(url_for('show_cluster', cluster_id=cluster_id))

# Recomended clusters - Algo

@app.route('/recommended_clusters')
def recommended_clusters():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    clusters = Cluster.query.all()
    user_skills = set(skill.lower() for skill in user.get_skills())
    user_desc_words = set(user.description.lower().split())
    scored = []
    for cluster in clusters:
        score = 0 
        tags_lower = set(tag.lower() for tag in cluster.get_tags())
        score += 3 * len(user_skills & tags_lower)
        if any(skill in cluster.target.lower() for skill in user_skills):
            score += 2 
        target_words = cluster.target.lower().split()
        skill_matches = sum(1 for skill in user_skills if any(skill in word for word in target_words))
        score += skill_matches 
        desc_matches = sum(1 for word in user_desc_words if word in target_words)
        score += desc_matches 
        score += 0.1 * len(cluster.get_members())
        scored.append((score, cluster))
    scored.sort(key=lambda x: x[0], reverse=True)
    matched_clusters = [c for score, c in scored if score > 0]
    return render_template('recommended.html', clusters=matched_clusters, user=user)
    
    
#simple endpoints

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')
    
@app.route('/logout')
def logout():
    session.clear()
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