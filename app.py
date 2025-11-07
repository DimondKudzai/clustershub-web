from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session,json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
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



@app.route('/register_update', methods=['GET', 'POST'])
def register_update():
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
            website = request.form.get('website', '').strip()
            second_website = request.form.get('second_website', '').strip()
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
            return redirect('/register_update')

        errors = []
        if password and password != confirm_password:
            errors.append("Passwords do not match")
        if len(skills) > 3:
            errors.append("You can add up to 3 skills only")
        if errors:
            session['notice'] = ', '.join(errors)
            return redirect('/register_update')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != session['user_id']:
            session['notice'] = "Email already exists"
            return redirect('/register_update')

        existing_username = User.query.filter_by(name=username).first()
        if existing_username and existing_username.id != session['user_id']:
            session['notice'] = "Username already taken"
            return redirect('/register_update')

        user = User.query.get(session['user_id'])
        if user:
            if username:
                user.name = username
            if full_name:
                user.full_name = full_name
            if email:
                user.email = email
            if location:
                user.location = location
            if website:
                user.website = website
            if second_website:
                user.second_website = second_website
            if skills:
                user.skills = json.dumps(skills)
            if password:
                user.password = generate_password_hash(password)
            db.session.commit()
        else:
            session['notice'] = "User not found"
            return redirect('/register_update')

        suggestion = Suggestion.query.first()
        if suggestion:
            existing_skills = suggestion.get_skills()
            suggestion.skills = json.dumps(list(set(existing_skills + skills)))
        else:
            suggestion = Suggestion(skills=json.dumps(skills))
            db.session.add(suggestion)
        db.session.commit()
        return redirect('/home')
    return render_template('set_profile.html', suggested_skills=suggested_skills, notice=notice)


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

@app.route('/startCluster', methods=['GET', 'POST'])
def startCluster():
    suggested = Suggestion.query.first()
    if suggested:
        suggested_skills = suggested.get_skills()
    else:
        suggested_skills = []
    notice = session.pop('notice', None)
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            skills = request.form.get('skills', '')
            if skills:
                try:
                    skills = json.loads(skills)
                except json.JSONDecodeError:
                    skills = []
            else:
                skills = []
            location = request.form.get('location', '').strip()
            status = request.form.get('status', '').strip()
            target = request.form.get('target', '').strip()
        except Exception as e:
            print(e)
            session['notice'] = "An error occurred"
            return redirect('/startCluster')

        errors = []
        if not name:
            errors.append("Cluster name is required")
        if not location:
            location = "International"
        if not status:
            errors.append("Product/service status is required")
        if not description:
            errors.append("Cluster description is required")
        if not skills:
            errors.append("At least one skill is required")
        if len(skills) > 10:
            errors.append("You can add up to 10 skills only")

        if errors:
            session['notice'] = ', '.join(errors)
            return redirect('/startCluster')

        # Get the user name from the session
        user = User.query.get(session['user_id'])
        author = user.name

        # Create the cluster
        cluster = Cluster(
            name=name,
            description=description,
            tags=json.dumps(skills),
            location=location,
            status=status,
            target=target,
            members=json.dumps([author]),
            author=author  # Store the user name as the author
        )
        db.session.add(cluster)
        db.session.commit()

        # Update the user's clusters
        created_clusters = json.loads(user.created_clusters)
        created_clusters.append(cluster.id)
        user.created_clusters = json.dumps(created_clusters)
        db.session.commit()

        return redirect('/clusters')
    return render_template('createCluster.html', suggested_skills=suggested_skills, notice=notice)
        


@app.route('/send_cluster_request/<cluster_id>', methods=['POST'])
def sent_cluster_request(cluster_id):
    title = request.form.get('title')
    message = request.form.get('message')
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        return redirect('/clusters')
    user = User.query.get(session['user_id'])
    if not user:
        return redirect('/login')
    requests = cluster.get_requests()
    new_request = {
        "chatId": len(requests) + 1,
        "title": title,
        "body": message,
        "author": user.name,
        "created": datetime.now(timezone.utc).isoformat(),
        "comments": []
    }
    requests.append(new_request)
    cluster.requests = json.dumps(requests)
    
    # Add cluster ID to user's clusters_requests
    user_clusters_requests = user.get_clusters_requests()
    user_clusters_requests.append(int(cluster_id))
    user.clusters_requests = json.dumps(user_clusters_requests)
    
    db.session.commit()
    return redirect(url_for('requested', cluster_id=cluster_id))



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
    show_clusters = [c for c in clusters if c.id in total_clusters]
    if show_clusters:
        return render_template('clusters.html', user=user, clusters=show_clusters, clustersCount=cluster_count)
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
        is_member = user.name in cluster.get_members()
        requested = id in user.get_clusters_requests()

        return render_template("cluster_detail.html", cluster=cluster, is_author=is_author, is_member=is_member, requested=requested)
    return jsonify({'error': 'Cluster not None, is_member=is_member'})
   
   
@app.route('/cluster_update/<int:id>', methods=['GET', 'POST'])
def cluster_updater(id):
    notice = session.pop('notice', None)
    cluster = Cluster.query.get(id)
    if not cluster:
        return redirect('/clusters')
    suggested = Suggestion.query.first()
    if suggested:
        suggested_skills = suggested.get_skills()
    else:
        suggested_skills = []
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            skills = request.form.get('skills', '')
            if skills:
                try:
                    skills = json.loads(skills)
                except json.JSONDecodeError:
                    skills = []
            else:
                skills = []
            location = request.form.get('location', '').strip()
            status = request.form.get('status', '').strip()
            target = request.form.get('target', '').strip()
        except Exception as e:
            print(e)
            session['notice'] = "An error occurred"
            return redirect('/cluster_update/' + str(id))
        errors = []
        if len(skills) > 10:
            errors.append("You can add up to 10 skills only")
        if errors:
            session['notice'] = ', '.join(errors)
            return redirect('/cluster_update/' + str(id))
        if name:
            cluster.name = name
        if description:
            cluster.description = description
        if skills:
            cluster.skills = json.dumps(skills)
        if location:
            cluster.location = location
        if status:
            cluster.status = status
        if target:
            cluster.target = target
        db.session.commit()
        return redirect('/clusters')
    return render_template('cluster_settings.html', cluster=cluster, suggested_skills=suggested_skills, notice=notice)
  
        
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

@app.route('/clusters/requests/<int:cluster_id>', methods=['GET', 'POST'])
def requested(cluster_id):
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        return "Cluster not found", 404
    return render_template('requests.html', cluster=cluster)   
   

@app.route('/clusters/requests/comment/<chatId>', methods=['POST'])
def requested_comment(chatId):
    text = request.form.get('text')
    user = User.query.get(session['user_id'])
    if not user:
        return redirect('/login')
    
    clusters = Cluster.query.all()
    for cluster in clusters:
        requests = cluster.get_requests()
        for req in requests:
            if str(req['chatId']) == chatId:
                req['comments'].append({
                    'user': user.name,
                    'text': text,
                    'timestamp': datetime.now(timezone.utc).isoformat()
                })
                cluster.requests = json.dumps(requests)
                db.session.commit()
                return redirect(url_for('requested', cluster_id=cluster.id))
    return "Request not found", 404
   
   
   
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
    
if __name__ == '__main__':
    app.run(debug=True)