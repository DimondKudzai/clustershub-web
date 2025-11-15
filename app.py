from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session,json,jsonify
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
#from services.appData import get_all_users, get_all_clusters, get_suggestions
from models import db
from config import Config
from models import User, Cluster, Suggestion # Import models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import uuid
import sqlite3
from sqlalchemy import func
from datetime import datetime

import humanize
from humanize import naturaltime

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = '2409'

db.init_app(app)

admin = Admin(app, name='Clusters Admin')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Cluster, db.session))
admin.add_view(ModelView(Suggestion, db.session))

app.jinja_env.filters['naturaltime'] = naturaltime


@app.template_filter('naturaltime')
def naturaltime_filter(timestamp):
    if isinstance(timestamp, str):
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    else:
        dt = timestamp
    return humanize.naturaltime(dt)
    
# HOME

@app.route('/')
def index():
    return redirect('/home')
    
    
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
    return render_template('dashboard.html',id=user.id, name=user.name, clustersCount=cluster_count, notificationsCount=unread_count)
    
    
# PROFILE
    
@app.route('/myProfile')
def myProfile():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')

    return render_template('profile.html', user=user)
        


# LOGIN HANDLER

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
        username = request.form['username'].strip().lower()
        password = request.form['password'].strip()
    except KeyError:
        return redirect(url_for('login'))
    
    user = User.query.filter((func.lower(User.name) == username) | (func.lower(User.email) == username)).first()
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
            description = request.form.get('description', '').strip()
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
        if not description:
            errors.append("Description is required")
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
            description=description,
            location=location,
            skills=json.dumps(skills),
            password=generate_password_hash(password),
            clusters_count=0,
           joined = datetime.utcnow(),
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
            description = request.form.get('description', '').strip()
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
            if description:
                user.description = description
            
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
        return redirect('/myProfile')
    return render_template('set_profile.html', suggested_skills=suggested_skills, notice=notice)


# Users

@app.route("/users")
def users():
    return jsonify(User.query.all())
    
@app.route("/users/<int:user_id>")
def getUser(user_id):
    user = User.query.get(user_id)
    if user:
        return render_template('profile.html', user=user)
    else:
        error = 'No user found'
        return render_template('error.html', error=error)
	    	    
	    
	    
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
        # Get the user ID from the session
        user_id = session['user_id']
        # Create the cluster
        cluster = Cluster(
            name=name,
            description=description,
            tags=json.dumps(skills),
            location=location,
            status=status,
            target=target,
            members=json.dumps([user_id]),
            author=user_id # Store the user ID as the author
        )
        db.session.add(cluster)
        db.session.commit()
        # Update the user's clusters
        user = User.query.get(user_id)
        created_clusters = json.loads(user.created_clusters)
        created_clusters.append(cluster.id)
        user.created_clusters = json.dumps(created_clusters)
        db.session.commit()
        return redirect('/clusters')
    return render_template('createCluster.html', suggested_skills=suggested_skills, notice=notice)
        

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
    error = "no clusters"
    return render_template('error.html', error=error)

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
        is_author = cluster.author == str(user.id)
        is_member = user.id in cluster.get_members()
        requested = id in user.get_clusters_requests()
        
        # Fetch the author user object
        author = User.query.get(cluster.author)
        
        # Fetch the member user objects
        members = [User.query.get(member_id) for member_id in cluster.get_members()]
        return render_template("cluster_detail.html", cluster=cluster, is_author=is_author, is_member=is_member, requested=requested, author=author, members=members, User=User)
    error = "No Cluster found"
    return render_template('error.html', error=error)
    
      
   
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
            cluster.tags = json.dumps(skills)
        if location:
            cluster.location = location
        if status:
            cluster.status = status
        if target:
            cluster.target = target
        db.session.commit()
        return redirect(url_for('getCluster', id=cluster.id))
        
    return render_template('cluster_settings.html', cluster=cluster, suggested_skills=suggested_skills, notice=notice)
  
  
@app.route('/clusters/<int:cluster_id>/delete', methods=['POST'])
def delete_cluster(cluster_id):
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    db.session.delete(cluster)
    db.session.commit()
    return redirect('/clusters')
  
  
@app.route('/clusters/<int:cluster_id>/members', methods=['GET'])
def get_cluster_members(cluster_id):
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    members = cluster.get_members()
    member_data = []
    for member_id in members:
        member = User.query.get(member_id)
        if member:
            member_data.append({'id': member.id, 'name': member.name})
    return render_template('cluster_members.html', cluster=cluster, members=member_data)
    
    
    
@app.route('/clusters/<int:cluster_id>/exit', methods=['POST'])
def exit_cluster(cluster_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    members = cluster.get_members()
    if user_id not in members:
        return redirect('/home')
    members.remove(user_id)
    cluster.set_members(members)
    db.session.commit()
    return redirect('/clusters')
    

@app.route('/clusters/<int:cluster_id>/remove-member/<int:member_id>', methods=['POST'])
def remove_cluster_member(cluster_id, member_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=_error)
    if int(cluster.author) != user_id:
        return redirect('/home')
    members = cluster.get_members()
    if int(member_id) not in members:
        return redirect('/home')
    members = [member for member in members if member != int(member_id)]
    cluster.set_members(members)
    db.session.commit()
    return redirect(url_for('getCluster', id=cluster_id))
    

@app.route('/clusters/<int:cluster_id>/members')
def cluster_members(cluster_id):
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    return render_template('cluster_members.html', cluster=cluster)
        
        
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
    messages.sort(key=lambda x: x['id'], reverse=True)
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

@app.route('/clusters/<int:cluster_id>/withdraw-request/<int:request_id>', methods=['POST'])
def withdraw_request(cluster_id, request_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    requests = cluster.get_requests()
    request_to_withdraw = next((r for r in requests if r['chatId'] == request_id), None)
    if not request_to_withdraw:
        error = "No Request found"
        return render_template('error.html', error=error)
    if request_to_withdraw['author'] != user_id:
        return redirect('/home')
    requests.remove(request_to_withdraw)
    cluster.set_requests(requests)
    user = User.query.get(user_id)
    user_clusters_requests = user.get_clusters_requests()
    if cluster_id in user_clusters_requests:
        user_clusters_requests.remove(cluster_id)
        user.clusters_requests = json.dumps(user_clusters_requests)
    db.session.commit()
    return redirect(url_for('user_requests'))
    

@app.route('/send_cluster_request/<cluster_id>', methods=['POST'])
def sent_cluster_request(cluster_id):
    title = request.form.get('title')
    message = request.form.get('message')
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        return redirect('/clusters')
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return redirect('/login')
    requests = cluster.get_requests()
    new_request = {
        "chatId": len(requests) + 1,
        "title": title,
        "body": message,
        "author": user_id,
        "created": datetime.utcnow().isoformat() + 'Z',
        "comments": []
    }
    requests.append(new_request)
    cluster.requests = json.dumps(requests)
    # Add cluster ID to user's clusters_requests
    user_clusters_requests = user.get_clusters_requests()
    user_clusters_requests.append(int(cluster_id))
    user.clusters_requests = json.dumps(user_clusters_requests)
    db.session.commit()
    return redirect(url_for('user_requests'))

@app.route('/clusters/requests/<int:cluster_id>', methods=['GET'])
def requested(cluster_id):
    if 'user_id' not in session:
        return redirect('/home')
    user_id = session['user_id']
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    if int(cluster.author) != user_id:
        return redirect('/home')
    requests = cluster.get_requests()
    if not requests:
        error = "no requests found"
        return render_template('error.html', error=error)
    
    for request in requests:
        author = User.query.get(request['author'])
        request['author_id'] = request['author']  # Add author's ID
        request['author_name'] = author.name if author else 'Unknown Author'
        for comment in request['comments']:
            comment['user'] = User.query.get(comment['user'])
    return render_template('requests.html', cluster=cluster, requests=requests)

@app.route('/clusters/requests/<int:cluster_id>/comment/<chatId>', methods=['POST'])
def requested_comment(cluster_id, chatId):
    text = request.form.get('text')
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return redirect('/login')
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    requests = cluster.get_requests()
    for req in requests:
        if str(req['chatId']) == chatId:
            req['comments'].append({
                'user': user_id,
                'text': text,
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            })
            cluster.requests = json.dumps(requests)
            db.session.commit()
            return redirect(url_for('user_requests'))
    error = "No Request found"
    return render_template('error.html', error=error)

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
    requested_clusters = []
    for c in clusters:
        if c.id in requested_ids:
            if isinstance(c.requests, str):
                requests = json.loads(c.requests or '[]')
            else:
                requests = c.requests or []
            user_requests = [r for r in requests if r['author'] == user_id]
            if user_requests:
                for request in user_requests:
                    author = User.query.get(request['author'])
                    request['author_name'] = author.name if author else 'Unknown Author'
                    for comment in request['comments']:
                        comment['user'] = User.query.get(comment['user'])
                cluster_data = c
                cluster_data.user_requests = user_requests
                requested_clusters.append(cluster_data)
    if requested_clusters:
        return render_template('user_request.html', user=user, clusters=requested_clusters, clustersCount=len(requested_clusters))
    error = "No Request found"
    return render_template('error.html', error=error)

@app.route('/clusters/<int:cluster_id>/requests/<int:request_id>/accept', methods=['POST'])
def accept_request(cluster_id, request_id):
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    requests = cluster.get_requests()
    request = next((r for r in requests if r['chatId'] == request_id), None)
    if not request:
        error = "No Request found"
        return render_template('error.html', error=error)
    # Add author to members
    members = cluster.get_members()
    members.append(request['author'])
    cluster.set_members(members)
    # Remove request from cluster requests
    requests.remove(request)
    if requests:
        cluster.set_requests(requests)
    else:
        cluster.set_requests([])
    # Remove request from user's clusters_requests
    user = User.query.get(request['author'])
    if user:
        user_clusters_requests = user.get_clusters_requests()
        user_clusters_requests.remove(cluster_id)
        user.clusters_requests = json.dumps(user_clusters_requests)
        # Send notification
        notification = {
            "id": len(user.get_messages()) + 1,
            "body": f"Your request to join {cluster.name} was accepted.",
            "read": False,
            "url": f"/clusters/{cluster.id}/chat",
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }
        user.set_messages(user.get_messages() + [notification])
    db.session.commit()
    return redirect(url_for('requested', cluster_id=cluster_id))
    

@app.route('/clusters/<int:cluster_id>/requests/<int:request_id>/decline', methods=['POST'])
def decline_request(cluster_id, request_id):
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    requests = cluster.get_requests()
    request = next((r for r in requests if r['chatId'] == request_id), None)
    if not request:
        error = "No Request found"
        return render_template('error.html', error=error)
    # Remove request from cluster requests
    requests.remove(request)
    if requests:
        cluster.set_requests(requests)
    else:
        cluster.set_requests([])
    # Remove request from user's clusters_requests
    user = User.query.get(request['author'])
    if user:
        user_clusters_requests = user.get_clusters_requests()
        user_clusters_requests.remove(cluster_id)
        user.clusters_requests = json.dumps(user_clusters_requests)
        # Send notification
        notification = {
            "id": len(user.get_messages()) + 1,
            "body": f"Your request to join {cluster.name} was declined. Here are your recommended Clusters",
            "read": False,
            "url": f"/recommended_clusters",
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        }
        user.set_messages(user.get_messages() + [notification])
    db.session.commit()
    return redirect(url_for('requested', cluster_id=cluster_id))

# conversations

@app.route('/clusters/<int:cluster_id>/chat', methods=['GET'])
def show_cluster(cluster_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    members = cluster.get_members()
    if user_id not in [User.query.filter_by(id=member).first().id for member in members]:
        return redirect('/home')
    
    conversations = cluster.get_conversations()
    for conversation in conversations:
        author = User.query.get(conversation['author'])
        conversation['author_id'] = conversation['author']
        conversation['author_name'] = author.name if author else 'Unknown Author'
        for comment in conversation['comments']:
            comment['user'] = User.query.get(comment['user'])
    
    return render_template('conversations.html', cluster=cluster, conversations=conversations)

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
        error = "No Cluster found"
        return render_template('error.html', error=error)
    conversations = cluster.get_conversations()
    thread = next((t for t in conversations if t['chatId'] == thread_id), None)
    if not thread:
        error = "Thread not found"
        return render_template('error.html', error=error)
    text = request.form['text']
    timestamp = datetime.utcnow().isoformat() + 'Z'
    thread['comments'].append({
        "user": user_id,  # Store the user ID instead of the name
        "text": text,
        "timestamp": timestamp
    })
    cluster.set_conversations(conversations)
    db.session.commit()
    return redirect(url_for('show_cluster', cluster_id=cluster_id))
    
@app.route('/clusters/<int:cluster_id>/threads', methods=['POST'])
def create_thread(cluster_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = User.query.get(user_id)
    if user is None:
        return redirect('/login')
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    title = request.form['title']
    body = request.form['text']
    timestamp = datetime.utcnow().isoformat() + 'Z'
    conversations = cluster.get_conversations()
    new_thread = {
        "title": title,
        "body": body,
        "author": user_id,  # Store the user ID instead of the name
        "chatId": len(conversations) + 1,
        "created": timestamp,
        "comments": []
    }
    conversations.append(new_thread)
    cluster.set_conversations(conversations)
    db.session.commit()
    return redirect(url_for('show_cluster', cluster_id=cluster_id))


@app.route('/clusters/<int:cluster_id>/updates', methods=['GET'])
def cluster_updates(cluster_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cluster = Cluster.query.get(cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    members = cluster.get_members()
    if user_id not in members:
        return redirect('/home')
    updates = cluster.get_updates()
    return render_template('updates.html', cluster=cluster, updates=updates)
       

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
    
    
# Extra endpoints

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')
    
@app.route('/error')
def error():
    return render_template('error.html', error=error)
    
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
  
  
if __name__ == '__main__':
    app.run(debug=True)