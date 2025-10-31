from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import sqlite3
from datetime import datetime
from flask import jsonify
from services.appData import get_all_users, get_all_clusters, get_suggestions

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

@app.route('/clusters/requests/<int:cluster_id>')
def requested(cluster_id):
    cluster = next((c for c in clusters if c['id'] == cluster_id), None)
    if not cluster:
        return "Cluster not found", 404
    return render_template('requests.html', cluster=cluster)
   


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
    
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/profile_settings')
def profile_settings():
    return render_template('set_profile.html')

@app.route('/cluster_settings')
def cluster_settings():
    return render_template('cluster_settings.html')
    
    
if __name__ == '__main__':
    app.run(debug=True)
