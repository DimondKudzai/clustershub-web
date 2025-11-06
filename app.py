from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session,json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import jsonify
#from services.appData import get_all_users, get_all_clusters, get_suggestions
from models import db
from config import Config
from models import User, Cluster, Suggestion # Import models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import sqlite3

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = '24091996'

db.init_app(app)

admin = Admin(app, name='Clusters Admin')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Cluster, db.session))
admin.add_view(ModelView(Suggestion, db.session))


@app.route('/')
def index():
    return redirect('/home')
    
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
        


#Authentication

# old handler
@app.route('/old_login_handler', methods=['POST'])
def old_login_handler():
    try:
        username = request.form['username'].strip()
        password = request.form['password'].strip()
    except KeyError:
        return redirect(url_for('login'))

    users = User.query.all()
    user = next((u for u in users if (u.name.strip().lower() == username.lower() or u.email.strip().lower() == username.lower()) and u.password == password), None)
    if user:
        session['user_id'] = user.id
        return redirect('/home')
    else:
        session['notice'] = "Invalid login details, retry or create an account"
        return redirect(url_for('login'))
        
# handler       
@app.route('/login_handler', methods=['POST'])
def login_handler():
    try:
        username = request.form['username'].strip()
        password = request.form['password'].strip()
    except KeyError:
        return redirect(url_for('login'))

    user = User.query.filter((User.name == username) | (User.email == username)).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect('/home')
    else:
        session['notice'] = "Invalid login details, retry or create an account"
        return redirect(url_for('login'))
        

@app.route('/login')
def login():
    notice = session.pop('notice', None)
    return render_template('auth.html', notice=notice)


@app.route('/register', methods=['GET', 'POST'])
def register():
    notice = session.pop('notice', None)
    suggested = Suggestion.query.first()
    if suggested:
        suggested_skills = suggested.get_skills()
    else:
        suggested_skills = []
    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            full_name = request.form.get('full_name', '').strip()
            email = request.form.get('email', '').strip()
            location = request.form.get('location', '').strip()
            skills = request.form.get('skills', '')
            if skills:
                try:
                    skills = json.loads(skills)
                except json.JSONDecodeError:
                    skills = []
            else:
                skills = []
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
        except Exception as e:
            print(e)
            session['notice'] = "An error occurred"
            return redirect('/register')

        errors = []
        if not username:
            errors.append("Username is required")
        if not full_name:
            errors.append("Full name is required")
        if not email:
            errors.append("Email is required")
        if not location:
            errors.append("Location is required")
        if not skills:
            errors.append("At least one skill is required")
        if not password:
            errors.append("Password is required")
        if not confirm_password:
            errors.append("Confirm password is required")
        if password != confirm_password:
            errors.append("Passwords do not match")
        if len(skills) > 3:
            errors.append("You can add up to 3 skills only")

        if errors:
            session['notice'] = ', '.join(errors)
            return redirect('/register')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            session['notice'] = "Email already exists"
            return redirect('/register')

        existing_username = User.query.filter_by(name=username).first()
        if existing_username:
            session['notice'] = "Username already taken"
            return redirect('/register')

        user = User(
            name=username,
            full_name=full_name,
            email=email,
            location=location,
            skills=json.dumps(skills),
            password=generate_password_hash(password),
            clusters_count=0,
            created_clusters=json.dumps([]),
            clusters_requests=json.dumps([]),
            notifications_count=0,
            messages=json.dumps([])
        )
        db.session.add(user)
        db.session.commit()

        suggestion = Suggestion.query.first()
        if suggestion:
            existing_skills = suggestion.get_skills()
            suggestion.skills = json.dumps(list(set(existing_skills + skills)))
        else:
            suggestion = Suggestion(skills=json.dumps(skills))
            db.session.add(suggestion)
        db.session.commit()

        session['user_id'] = user.id
        return redirect('/home')
    return render_template('register.html', suggested_skills=suggested_skills, notice=notice)

# Users

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
        is_author = cluster.author == user.name
        is_member = user.id in cluster.get_members()
        requested = id in user.get_clusters_requests()

        return render_template("cluster_detail.html", cluster=cluster, is_author=is_author, is_member=is_member, requested=requested)
    return jsonify({'error': 'Cluster not None, is_member=is_member'})
   
        
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