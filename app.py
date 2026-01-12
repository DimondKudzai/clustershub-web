from flask import Flask, request, redirect, url_for, render_template, send_from_directory, session,json,jsonify,send_file
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from models import db
from config import Config
from models import User, Cluster, Suggestion # models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import uuid
import sqlite3
from sqlalchemy import func
from datetime import datetime
from functools import wraps
import humanize
from humanize import naturaltime
import re
from markupsafe import Markup, escape
from flask_mail import Mail, Message
from flask import render_template_string
from flask_login import current_user
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
from email.message import EmailMessage
import smtplib
import logging
from flask_login import LoginManager
import math
from collections import Counter
import pytz
import requests as http_requests

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = Config.SECRET_KEY

REMOTE_META_URL = 'http://smartlearning.liveblog365.com/backups/db_meta.php'
REMOTE_DB_URL = 'http://smartlearning.liveblog365.com/backups/clusters.db'
REMOTE_UPLOAD_URL = 'http://smartlearning.liveblog365.com/backups/upload_db.php'
DB_PATH = '/tmp/clusters.db'
SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/clusters.db")

def get_local_timestamp():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT last_updated FROM meta WHERE id = 1")
        ts = c.fetchone()[0]
        conn.close()
        return ts
    except:
        return None

def get_remote_timestamp():
    try:
        r = http_requests.get(REMOTE_META_URL, timeout=10)
        return r.json().get('last_updated')
    except:
        return None

def download_remote_db():
    r = http_requests.get(REMOTE_DB_URL)
    with open(DB_PATH, 'wb') as f:
        f.write(r.content)

def upload_local_db():
    with open(DB_PATH, 'rb') as f:
        r = http_requests.post(REMOTE_UPLOAD_URL, files={'file': f})
        print(r.text)

def update_local_timestamp():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now_utc = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
    c.execute("UPDATE meta SET last_updated = ? WHERE id = 1", (now_utc,))
    conn.commit()
    conn.close()
    
if not os.path.exists(DB_PATH):
    download_remote_db()
    
login_manager = LoginManager()
login_manager.init_app(app)
db.init_app(app)

"""
app.config['MAIL_SERVER'] = Config.MAIL_SERVER
app.config['MAIL_PORT'] = Config.MAIL_PORT
app.config['MAIL_USE_TLS'] = Config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = Config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = Config.MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = Config.MAIL_DEFAULT_SENDER

mail = Mail(app)
"""

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1 or 2

admin = Admin(app, name='Clusters Admin')
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Cluster, db.session))
admin.add_view(MyModelView(Suggestion, db.session))

# Decorator to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            session['next'] = request.url
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
    

app.jinja_env.filters['naturaltime'] = naturaltime

from itsdangerous import URLSafeTimedSerializer

# Password reset
def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, max_age=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        return serializer.loads(token, salt='password-reset-salt', max_age=max_age)
    except:
        return None

@app.template_filter('naturaltime')
def naturaltime_filter(timestamp):
    if isinstance(timestamp, str):
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    elif timestamp.tzinfo is None:
        dt = timestamp.replace(tzinfo=timezone.utc)
    else:
        dt = timestamp
    return humanize.naturaltime(dt)   
    
"""

# Create a URLSafeTimedSerializer for generating and verifying tokens
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generate_confirmation_token(email):
    return ts.dumps(email, salt='confirm-email')

def verify_confirmation_token(token, expiration=3600):
    try:
        email = ts.loads(token, salt='confirm-email', max_age=expiration)
    except:
        return None
    return email

@app.route('/send-confirmation-email', methods=['POST', 'GET'])
@login_required
def send_confirmation_email():
    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    if not user:
        error = "User not logged in"
        return redirect(url_for('error', error=error))
    if user.confirm_email == 1:
        return redirect(url_for('home'))
    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)

    # Create the email message
    msg = Message('Confirm Your Email Address', 
                  sender='noreply@clustershub.co.zw', 
                  recipients=[user.email])
    msg.html = render_template('email_confirm_email.html', 
                               confirm_url=confirm_url, 
                               user=user)

    # Send the email
    mail.send(msg)

    return render_template('confirm.html', message='A confirmation email has been sent to your email address. Please open your mail box and click confirm to finish registration. Link expires in 60 minutes')
    

@app.route('/confirm/<token>')
def confirm_email(token):
    email = verify_confirmation_token(token)
    if not email:
        error = "Token expired or invalid"
        return redirect(url_for('error'), error=error)
        
    user = User.query.filter_by(email=email).first()
    if user:
        user.confirm_email = int(1)
        db.session.commit()
        return redirect(url_for('home'))
    erorr = "User not found"
    return redirect(url_for('error'), error=error)
    
    
@app.before_request
def check_confirmed():
    exempt_routes = ['login', 'logout', 'confirm_email', 'send_confirmation_email', 'resend_confirmation_email', 'static']
    if request.endpoint in exempt_routes or request.endpoint is None:
        return  # Skip check for exempt routes
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)
        if user and str(user.confirm_email) != '1':
            if request.endpoint != 'send_confirmation_email':
                return redirect(url_for('send_confirmation_email'))

@app.route('/resend-confirmation-email')
@login_required
def resend_confirmation_email():
    if current_user.confirm_email:
        return redirect(url_for('dashboard'))
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    msg = Message('Confirm Your Email Address', 
                  sender='noreply@clustershub.co.zw', 
                  recipients=[current_user.email])
    msg.html = render_template('email/confirm_email.html', 
                               confirm_url=confirm_url, 
                               user=current_user)
    mail.send(msg)
    message = "We have sent you an email. Please click on the link sent to you to confirm your account. Please check your mailbox and click on the link before it expires in 60 minutes."
    return render_template('confirm.html', message=message)
"""

# HOME
@app.route('/')
def index():
    return redirect('/home')
    
    
@app.route('/home')
def home():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = db.session.get(User,user_id)
    if user is None:
        return redirect('/login')

    created_clusters = user.get_created_clusters()
    cluster_count = len(created_clusters)
    messages = user.get_messages()
    # Count unread
    unread_count = sum(1 for m in messages if not m.get("read", False))
    return render_template('dashboard.html',id=user.id, name=user.name, clustersCount=cluster_count, notificationsCount=unread_count)  


# LOGIN HANDLER
@app.route('/tlogin_handler', methods=['POST'])
def tlogin_handler():
    try:
        username = request.form['username'].strip().lower()
        password = request.form['password'].strip()
    except KeyError:
        return redirect(url_for('login'))
    
    user = User.query.filter((func.lower(User.name) == username) | (func.lower(User.email) == username)).first()
    if user and user.password == password:
        session['user_id'] = user.id
        return redirect('/home')
    else:
        session['notice'] = "Invalid login details, retry or create an account"
        return redirect(url_for('login'))
        
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
        #login_user(user)
        next_url = session.pop('next', None)
        if next_url:
            return redirect(next_url)
        else:
            return redirect('/home')
    else:
        session['notice'] = "Invalid login details, retry or create an account"
        return redirect(url_for('login'))
        

@app.route('/login')
def login():
    notice = session.pop('notice', None)
    return render_template('auth.html', notice=notice)


@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            hint = user.password_recovery
            return render_template('forgot.html', hint=hint)
        else:
            error = "Email address not registered"
            return render_template('error.html', error=error)
    return render_template('forgot.html')
    
# Register
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
            password_recovery = request.form.get('password_recovery', '').strip()
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
        if not password_recovery:
            errors.append("Secure Password Hint is required")
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
            password_recovery=password_recovery,
            skills=json.dumps(skills),
            password=generate_password_hash(password),
            clusters_count=0,
            joined=datetime.now(timezone.utc),
            confirm_email=0,
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
        
        # Send notification
        notification = {
        "id": len(user.get_messages()) + 1,
        "body": f"Hello {username}, Welcome to your first day on Clusters Hub. Get started with work by Creating a Cluster or joining Clusters. Please don't forget to spread the good news to everyone who might benefit from using Clusters Hub. Here are your recommended Clusters.",
        "read": False,
        "url": f"/recommended_clusters",
        "timestamp": datetime.now(timezone.utc).isoformat()
        }
        user.set_messages(user.get_messages() + [notification])
        db.session.commit()
        
        session['user_id'] = user.id
        #login_user(user)
        return redirect('/home')
    return render_template('register.html', suggested_skills=suggested_skills, notice=notice)


@app.route('/register_update', methods=['GET', 'POST'])
@login_required
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
            password_recovery = request.form.get('password_recovery', '').strip()
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
            session['notice'] = "Email already registered"
            return redirect('/register_update')
            
        existing_email = User.query.filter_by(email=email).first()
        if existing_user and existing_user.email != session['user_id']:
            session['notice'] = "Email already registered"
            return redirect('/register_update')
    
        existing_username = User.query.filter_by(name=username).first()
        if existing_username and existing_username.id != session['user_id']:
            session['notice'] = "Username already taken"
            return redirect('/register_update')

        user = db.session.get(User, session['user_id'])
        if user:
            if username:
                user.name = username
            if full_name:
                user.full_name = full_name
            if email:
                user.email = email
                user.confirm_email = int(0)
            if location:
                user.location = location
            if password_recovery:
                user.password_recovery = password_recovery
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
@app.route('/myProfile')
@login_required
def myProfile():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = db.session.get(User, user_id)
    if user is None:
        return redirect('/login')

    return render_template('myProfile.html', user=user)
        

@app.route("/users")
@login_required
def users():
    return jsonify(User.query.all())
    
    
@app.route("/users/<int:user_id>")
@login_required
def getUser(user_id):
    user = db.session.get(User, user_id)
    if user:
        return render_template('profile.html', user=user)
    else:
        error = 'No user found'
        return render_template('error.html', error=error)
	    	    
	    
# Clusters
@app.route('/startCluster', methods=['GET', 'POST'])
@login_required
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
            author=user_id  # Store the user ID as the author
        )
        db.session.add(cluster)
        db.session.commit()
        # Update the user's clusters
        user = db.session.get(User, user_id)
        created_clusters = user.get_created_clusters()
        created_clusters.append(cluster.id)
        user.set_created_clusters(created_clusters)

        user_clusters = user.get_joined()
        user_clusters.append(cluster.id)
        user.set_joined(user_clusters)

        db.session.commit()
        # Send notification
        notification = {
            "id": len(user.get_messages()) + 1,
            "body": f"Congratulations, You have successfully created Cluster - { name }. As the author of the Cluster your responsiblity is to manage the Cluster. Did you know sharing your Cluster online increases member quality by 4 times?. Here are your Clusters.",
            "read": False,
            "url": f"/clusters",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        user.set_messages(user.get_messages() + [notification])
        db.session.commit()
        updates = {
            "message": f"{cluster.name} created by Author.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        cluster.set_updates(cluster.get_updates() + [updates])
        db.session.commit()
        return redirect('/clusters')
    return render_template('createCluster.html', suggested_skills=suggested_skills, notice=notice)
        

@app.route('/clusters')
@login_required
def clusters():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = db.session.get(User, user_id)
    if user is None:
        return redirect('/login')

    clusters = Cluster.query.all()
    created_clusters = user.get_created_clusters()
    joined_clusters = user.get_joined()
    requested_clusters = user.get_clusters_requests()
    total_clusters = joined_clusters + created_clusters + requested_clusters
    cluster_count = len(total_clusters)
    show_clusters = [c for c in clusters if c.id in total_clusters]
    if show_clusters:
        return render_template('clusters.html', user=user, clusters=show_clusters, clustersCount=cluster_count)
    error = "no clusters"
    return render_template('error.html', error=error)


@app.route("/clusters/<int:id>")
@login_required
def getCluster(id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = db.session.get(User, user_id)
    if user is None:
        return redirect('/login')
    cluster = db.session.get(Cluster, id)
    if cluster:
        is_author = cluster.author == str(user.id)
        is_member = user.id in cluster.get_members()
        requested = id in user.get_clusters_requests()
        
        # Fetch the author user object
        author = db.session.get(User, cluster.author)
        
        # Fetch the member user objects
        members = [db.session.get(User, member_id) for member_id in cluster.get_members()]
        return render_template("cluster_detail.html", cluster=cluster, is_author=is_author, is_member=is_member, requested=requested, author=author, members=members, User=User)
    error = "No Cluster found"
    return render_template('error.html', error=error)
    
        
@app.route('/cluster_update/<int:id>', methods=['GET', 'POST'])
@login_required
def cluster_updater(id):
    notice = session.pop('notice', None)
    cluster = db.session.get(Cluster, id)
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
@login_required
def delete_cluster(cluster_id):
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)

    members = cluster.get_members()
    cluster_author = db.session.get(User, cluster.author)

    # Remove cluster from member_clusters of all members
    for member_id in members:
        member = db.session.get(User, member_id)
        if member:
            member_joined_clusters = member.get_joined()
            member_joined_clusters.remove(cluster_id)
            member.set_joined(member_joined_clusters)

    db.session.delete(cluster)
    db.session.commit()

    # Send notification to all cluster members excluding the author
    for member_id in members:
        if member_id != cluster.author:  # Check if the member is not the cluster author
            member = db.session.get(User, member_id)
            if member:
                notification = {
                    "id": len(member.get_messages()) + 1,
                    "body": f"{cluster.name} was deleted by its Author. Here are your recommended Clusters",
                    "read": False,
                    "url": f"/recommended_clusters",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                member.set_messages(member.get_messages() + [notification])
                db.session.commit()

    return redirect('/clusters')
  
  
@app.route('/clusters/<int:cluster_id>/members', methods=['GET'])
@login_required
def get_cluster_members(cluster_id):
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    members = cluster.get_members()
    member_data = []
    for member_id in members:
        member = db.session.get(User, member_id)
        if member:
            member_data.append({'id': member.id, 'name': member.name})
    return render_template('cluster_members.html', cluster=cluster, members=member_data)
    
        
@app.route('/clusters/<int:cluster_id>/exit', methods=['POST'])
@login_required
def exit_cluster(cluster_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    members = cluster.get_members()
    if user_id not in members:
        return redirect('/home')
    members.remove(user_id)
    cluster.set_members(members)
    
    user = db.session.get(User, user_id)
    if user is None:
        return redirect('/login')
    
    # Remove cluster from user's joined clusters
    user_joined_clusters = user.get_joined()
    user_joined_clusters.remove(cluster_id)
    user.set_joined(user_joined_clusters)
    
    db.session.commit()
    
    # Send notification
    notification = {
        "id": len(user.get_messages()) + 1,
        "body": f"You exited {cluster.name}. Here are your recommended Clusters",
        "read": False,
        "url": f"/recommended_clusters",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    user.set_messages(user.get_messages() + [notification])
    db.session.commit()
    updates = {
        "message": f"{user.name} left this Cluster",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    cluster.set_updates(cluster.get_updates() + [updates])
    db.session.commit()
    return redirect('/clusters')
    

@app.route('/clusters/<int:cluster_id>/remove-member/<int:member_id>', methods=['POST'])
@login_required
def remove_cluster_member(cluster_id, member_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    user = db.session.get(User, user_id)  # Retrieve the user object
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    if int(cluster.author) != user_id:
        return redirect('/home')
    members = cluster.get_members()
    if int(member_id) not in members:
        return redirect('/home')
    removed_member = db.session.get(User, member_id)
    members = [member for member in members if member != int(member_id)]
    cluster.set_members(members)
    
    # Remove cluster from removed member's joined clusters
    removed_member_joined_clusters = removed_member.get_joined()
    removed_member_joined_clusters.remove(cluster_id)
    removed_member.set_joined(removed_member_joined_clusters)
    
    db.session.commit()
    # Send notification
    notification = {
        "id": len(user.get_messages()) + 1,
        "body": f"You successfully removed {removed_member.name} from Cluster - {cluster.name}.",
        "read": False,
        "url": f"/clusters/{cluster_id}",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    user.set_messages(user.get_messages() + [notification])
    db.session.commit()
    second_notification = {
        "id": len(removed_member.get_messages()) + 1,
        "body": f"You were removed from Cluster - {cluster.name}.",
        "read": False,
        "url": f"/clusters/{cluster_id}",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    removed_member.set_messages(removed_member.get_messages() + [second_notification])
    db.session.commit()
    updates = {
        "message": f"{removed_member.name} was removed from this Cluster by author",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    cluster.set_updates(cluster.get_updates() + [updates])
    db.session.commit()
    return redirect(url_for('getCluster', id=cluster_id))
    

@app.route('/clusters/<int:cluster_id>/members')
@login_required
def cluster_members(cluster_id):
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    return render_template('cluster_members.html', cluster=cluster)
        
        
# Notifications                
@app.route("/notifications")
@login_required
def notifications():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = db.session.get(User, user_id)
    if user is None:
        return redirect('/login')
    messages = user.get_messages()
    messages.sort(key=lambda x: x['id'], reverse=True)
    return render_template("notifications.html", messages=messages)
    

@app.route("/notifications/read/<int:msg_id>")
@login_required
def mark_read(msg_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = db.session.get(User, user_id)
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
@login_required
def withdraw_request(cluster_id, request_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cluster = db.session.get(Cluster, cluster_id)
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
    user = db.session.get(User, user_id)
    user_clusters_requests = user.get_clusters_requests()
    if cluster_id in user_clusters_requests:
        user_clusters_requests.remove(cluster_id)
        user.clusters_requests = json.dumps(user_clusters_requests)
    db.session.commit()
    
    # Send notification
    notification = {
    "id": len(user.get_messages()) + 1,
    "body": f"You successfully withdrew your request to join - {cluster.name}.",
    "read": False,
    "url": f"/clusters/{cluster_id}",
    "timestamp": datetime.now(timezone.utc).isoformat()
    }
    user.set_messages(user.get_messages() + [notification])
    db.session.commit()

    return redirect(url_for('user_requests'))
    

@app.route('/send_cluster_request/<cluster_id>', methods=['POST'])
@login_required
def sent_cluster_request(cluster_id):
    title = request.form.get('title')
    message = request.form.get('message')
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        return redirect('/clusters')
    user_id = session['user_id']
    user = db.session.get(User, user_id)
    if not user:
        return redirect('/login')
    requests = cluster.get_requests()
    new_request = {
        "chatId": len(requests) + 1,
        "title": title,
        "body": message,
        "author": user_id,
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
    # Send notification to cluster author
    cluster_author = db.session.get(User, cluster.author)
    notification = {
        "id": len(cluster_author.get_messages()) + 1,
        "body": f"{user.name} requested to join your Cluster - {cluster.name}.",
        "read": False,
        "url": f"/clusters/requests/{cluster.id}",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    cluster_author.set_messages(cluster_author.get_messages() + [notification])
    db.session.commit()
    return redirect(url_for('user_requests'))


@app.route('/clusters/requests/<int:cluster_id>', methods=['GET'])
@login_required
def requested(cluster_id):
    if 'user_id' not in session:
        return redirect('/home')
    user_id = session['user_id']
    cluster = db.session.get(Cluster, cluster_id)
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
        author = db.session.get(User, request['author'])
        request['author_id'] = request['author']  # Add author's ID
        request['author_name'] = author.name if author else 'Unknown Author'
        for comment in request['comments']:
            comment['user'] = db.session.get(User, comment['user'])
    return render_template('requests.html', cluster=cluster, requests=requests)


@app.route('/clusters/requests/<int:cluster_id>/comment/<chatId>', methods=['POST'])
@login_required
def requested_comment(cluster_id, chatId):
    text = request.form.get('text')
    user_id = session['user_id']
    user = db.session.get(User, user_id)
    if not user:
        return redirect('/login')
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    requests = cluster.get_requests()
    for req in requests:
        if str(req['chatId']) == chatId:
            req['comments'].append({
                'user': user_id,
                'text': text,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            cluster.requests = json.dumps(requests)
            db.session.commit()
            # Send notification to the request author (only if not the same user)
            request_author = db.session.get(User, req['author'])
            if request_author.id != user_id:
                notification = {
                    "id": len(request_author.get_messages()) + 1,
                    "body": f"{user.name} replied to your request to join {cluster.name}.",
                    "read": False,
                    "url": f"/user_requests",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                request_author.set_messages(request_author.get_messages() + [notification])
                db.session.commit()
            return redirect(url_for('requested', cluster_id=cluster_id))
    error = "No Request found"
    return render_template('error.html', error=error)
    
    
@app.route('/user_clusters/requests/<int:cluster_id>/comment/<chatId>', methods=['POST'])
@login_required
def user_requested_comment(cluster_id, chatId):
    text = request.form.get('text')
    user_id = session['user_id']
    user = db.session.get(User, user_id)
    if not user:
        return redirect('/login')
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    requests = cluster.get_requests()
    for req in requests:
        if str(req['chatId']) == chatId:
            req['comments'].append({
                'user': user_id,
                'text': text,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            cluster.requests = json.dumps(requests)
            db.session.commit()
            # Send notification to the request author (only if not the same user)
            request_author = db.session.get(User, req['author'])
            if request_author.id != user_id:
                notification = {
                    "id": len(request_author.get_messages()) + 1,
                    "body": f"{user.name} replied to your request to join {cluster.name}.",
                    "read": False,
                    "url": f"/user_requests",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                request_author.set_messages(request_author.get_messages() + [notification])
                db.session.commit()
            return redirect(url_for('user_requests'))
    error = "No Request found"
    return render_template('error.html', error=error)


@app.route('/user_requests')
@login_required
def user_requests():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = db.session.get(User, user_id)
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
                    author = db.session.get(User, request['author'])
                    request['author_name'] = author.name if author else 'Unknown Author'
                    for comment in request['comments']:
                        comment['user'] = db.session.get(User, comment['user'])
                cluster_data = c
                cluster_data.user_requests = user_requests
                requested_clusters.append(cluster_data)
    if requested_clusters:
        return render_template('user_request.html', user=user, clusters=requested_clusters, clustersCount=len(requested_clusters))
    error = "No Request found"
    return render_template('error.html', error=error)


@app.route('/clusters/<int:cluster_id>/requests/<int:request_id>/accept', methods=['POST'])
@login_required
def accept_request(cluster_id, request_id):
    cluster = db.session.get(Cluster, cluster_id)
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
    user = db.session.get(User, request['author'])
    if user:
        user_clusters_requests = user.get_clusters_requests()
        user_clusters_requests.remove(cluster_id)
        user.set_clusters_requests(user_clusters_requests)
        
        # Add cluster to user's joined clusters
        user_joined_clusters = user.get_joined()
        user_joined_clusters.append(cluster_id)
        user.set_joined(user_joined_clusters)
        
        # Send notification
        notification = {
            "id": len(user.get_messages()) + 1,
            "body": f"Congratulations your request to join {cluster.name} was accepted. Start contributing.",
            "read": False,
            "url": f"/clusters/{cluster.id}/chat",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        user.set_messages(user.get_messages() + [notification])
        db.session.commit()
        updates = {
            "message": f"{user.name} was added to this Cluster.",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        cluster.set_updates(cluster.get_updates() + [updates])
        db.session.commit()
    return redirect(url_for('requested', cluster_id=cluster_id))
    

@app.route('/clusters/<int:cluster_id>/requests/<int:request_id>/decline', methods=['POST'])
@login_required
def decline_request(cluster_id, request_id):
    cluster = db.session.get(Cluster, cluster_id)
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
    user = db.session.get(User, request['author'])
    if user:
        user_clusters_requests = user.get_clusters_requests()
        user_clusters_requests.remove(cluster_id)
        user.clusters_requests = json.dumps(user_clusters_requests)
        # Send notification
        notification = {
            "id": len(user.get_messages()) + 1,
            "body": f"Your request to join {cluster.name} was declined by its author. Here are your recommended Clusters.",
            "read": False,
            "url": f"/recommended_clusters",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        user.set_messages(user.get_messages() + [notification])
    db.session.commit()
    return redirect(url_for('requested', cluster_id=cluster_id))


# conversations
@app.route('/clusters/<int:cluster_id>/chat', methods=['GET'])
@login_required
def show_cluster(cluster_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    members = cluster.get_members()
    if user_id not in [User.query.filter_by(id=member).first().id for member in members]:
        return redirect('/home')
    
    conversations = cluster.get_conversations()
    for conversation in conversations:
        author = db.session.get(User, conversation['author'])
        conversation['author_id'] = conversation['author']
        conversation['author_name'] = author.name if author else 'Unknown Author'
        for comment in conversation['comments']:
            comment['user'] = db.session.get(User, comment['user'])
    
    return render_template('conversations.html', cluster=cluster, conversations=conversations)


@app.route('/clusters/<int:cluster_id>/threads/<int:thread_id>/comments', methods=['POST'])
@login_required
def post_comment(cluster_id, thread_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = db.session.get(User, user_id)
    if user is None:
        return redirect('/login')
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    conversations = cluster.get_conversations()
    thread = next((t for t in conversations if t['chatId'] == thread_id), None)
    if not thread:
        error = "Thread not found"
        return render_template('error.html', error=error)
    text = request.form['text']
    timestamp = datetime.now(timezone.utc).isoformat()
    thread['comments'].append({
        "user": user_id,  # Store the user ID instead of the name
        "text": text,
        "timestamp": timestamp
    })
    cluster.set_conversations(conversations)
    db.session.commit()
    
    # Send notification to the thread author (excluding the comment author)
    thread_author = db.session.get(User, thread['author'])
    if thread_author.id != user_id:  # Check if the comment author is not the thread author
        notification = {
            "id": len(thread_author.get_messages()) + 1,
            "body": f"{user.name} commented on your thread - {thread['title']}. Check what they said.",
            "read": False,
            "url": f"/clusters/{cluster_id}/chat",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        thread_author.set_messages(thread_author.get_messages() + [notification])
        db.session.commit()
    return redirect(url_for('show_cluster', cluster_id=cluster_id))
    
    
@app.route('/clusters/<int:cluster_id>/threads', methods=['POST'])
@login_required
def create_thread(cluster_id):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = db.session.get(User, user_id)
    if user is None:
        return redirect('/login')
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    title = request.form['title']
    body = request.form['text']
    timestamp = datetime.now(timezone.utc).isoformat()
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
    
    # Send notification to all cluster members excluding the thread author
    members = cluster.get_members()
    for member_id in members:
        if member_id != user_id:  # Check if the member is not the thread author
            member = db.session.get(User, member_id)
            if member:
                notification = {
                    "id": len(member.get_messages()) + 1,
                    "body": f"{user.name} created a new Thread titled '{title}' in Cluster - {cluster.name}.",
                    "read": False,
                    "url": f"/clusters/{cluster_id}/chat",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                member.set_messages(member.get_messages() + [notification])
                db.session.commit()
    updates = {
        "message": f"Thread '{title}' created by {user.name}.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    cluster.set_updates(cluster.get_updates() + [updates])
    db.session.commit()
    return redirect(url_for('show_cluster', cluster_id=cluster_id))


@app.route('/clusters/<int:cluster_id>/updates', methods=['GET'])
@login_required
def cluster_updates(cluster_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    cluster = db.session.get(Cluster, cluster_id)
    if not cluster:
        error = "No Cluster found"
        return render_template('error.html', error=error)
    members = cluster.get_members()
    if user_id not in members:
        return redirect('/home')
    updates = cluster.get_updates()
    return render_template('updates.html', cluster=cluster, updates=updates)
       

# Recomended clusters

@app.route('/recommended_clusters')
@login_required
def recommended_clusters():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = db.session.get(User, user_id)
    if user is None:
        return redirect('/login')

    def tokenize(text):
        return re.findall(r'[a-zA-Z0-9_]+', text.lower()) if text else []

    def compute_tf(text_tokens):
        tf = Counter(text_tokens)
        total_terms = len(text_tokens)
        return {word: count / total_terms for word, count in tf.items()}

    def compute_idf(documents):
        N = len(documents)
        idf = {}
        all_tokens = set(token for doc in documents for token in set(doc))
        for token in all_tokens:
            containing_docs = sum(1 for doc in documents if token in doc)
            idf[token] = math.log((N + 1) / (containing_docs + 1)) + 1  # Smoothed
        return idf

    def compute_tfidf(tf, idf):
        return {word: tf[word] * idf[word] for word in tf}

    def cosine_sim(vec1, vec2):
        common = set(vec1) & set(vec2)
        num = sum(vec1[x] * vec2[x] for x in common)
        denom1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        denom2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        if denom1 == 0 or denom2 == 0:
            return 0.0
        return num / (denom1 * denom2)

    def semantic_similarity_score(text1, text2):
        tokens1 = tokenize(text1)
        tokens2 = tokenize(text2)
        idf = compute_idf([tokens1, tokens2])
        tfidf1 = compute_tfidf(compute_tf(tokens1), idf)
        tfidf2 = compute_tfidf(compute_tf(tokens2), idf)
        return cosine_sim(tfidf1, tfidf2)

    user_skills = [skill.lower() for skill in user.get_skills()]
    user_desc_words = tokenize(user.description)
    user_location = user.location.lower() if user.location else ''
    user_text = ' '.join(user_skills + user_desc_words + [user_location])

    scored = []
    for cluster in Cluster.query.all():
        tags = [tag.lower() for tag in cluster.get_tags()]
        target = cluster.target.lower() if cluster.target else ''
        cluster_desc = cluster.description.lower() if cluster.description else ''
        cluster_location = cluster.location.lower() if cluster.location else ''
        target_words = tokenize(target)
        cluster_desc_words = tokenize(cluster_desc)
        score = 0
        # Exact skill/tag match
        score += 3 * len(set(user_skills) & set(tags))
        # Partial skill in target string
        score += sum(1 for skill in user_skills if skill in target)
        # Substring match in individual target words
        score += sum(1 for skill in user_skills if any(skill in word for word in target_words))
        # Word overlap in description
        score += sum(1 for word in user_desc_words if word in cluster_desc_words)
        # Location match
        if user_location and cluster_location and (user_location in cluster_location or cluster_location in user_location):
            score += 5
        # Semantic similarity
        cluster_text = ' '.join(tags + [target, cluster_desc, cluster_location])
        score += semantic_similarity_score(user_text, cluster_text) * 5
        # Member count bonus
        score += 0.1 * len(cluster.get_members())
        if score > 0:
            scored.append((score, cluster))
    scored.sort(key=lambda x: x[0], reverse=True)
    matched_clusters = [c for score, c in scored]
    return render_template('recommended.html', clusters=matched_clusters, user=user)
    
"""
@app.route('/recommended_clusters')
@login_required
def recommended_clusters():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')

    user = db.session.get(User, user_id)
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
    

# ai powered matching

@app.route('/ai_recommended_clusters')
@login_required
def ai_recommended_clusters():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = db.session.get(User, user_id)
    if user is None:
        return redirect('/login')

    def tokenize(text):
        return re.findall(r'[a-zA-Z0-9_]+', text.lower()) if text else []

    user_skills = [skill.lower() for skill in user.get_skills()]
    user_desc_words = tokenize(user.description)
    user_location = user.location.lower() if user.location else ''
    user_text = ' '.join(user_skills + user_desc_words + [user_location])

    def semantic_similarity_score(text1, text2):
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        vectors = vectorizer.fit_transform([text1, text2])
        return cosine_similarity(vectors[0], vectors[1])[0][0]

    scored = []
    for cluster in Cluster.query.all():
        tags = [tag.lower() for tag in cluster.get_tags()]
        target = cluster.target.lower() if cluster.target else ''
        cluster_desc = cluster.description.lower() if cluster.description else ''
        cluster_location = cluster.location.lower() if cluster.location else ''
        target_words = tokenize(target)
        cluster_desc_words = tokenize(cluster_desc)

        score = 0
        # Exact skill/tag match
        score += 3 * len(set(user_skills) & set(tags))
        # Partial skill in target string
        score += sum(1 for skill in user_skills if skill in target)
        # Substring match in individual target words
        score += sum(1 for skill in user_skills if any(skill in word for word in target_words))
        # Word overlap in description
        score += sum(1 for word in user_desc_words if word in cluster_desc_words)
        # Location match
        if user_location and cluster_location and (user_location in cluster_location or cluster_location in user_location):
            score += 5
        # Semantic similarity
        cluster_text = ' '.join(tags + [target, cluster_desc, cluster_location])
        score += semantic_similarity_score(user_text, cluster_text) * 5
        # Member count bonus
        score += 0.1 * len(cluster.get_members())

        if score > 0:
            scored.append((score, cluster))

    scored.sort(key=lambda x: x[0], reverse=True)
    matched_clusters = [c for score, c in scored]

    return render_template('recommended.html', clusters=matched_clusters, user=user)
"""
    
# Extra endpoints

@app.route('/admin/analytics')
@login_required
def admin_analytics():
    if session.get('user_id') > 2:
        return redirect('/home')

    total_users = User.query.count()
    total_clusters = Cluster.query.count()
    
    total_requests = sum(len(cluster.get_requests()) for cluster in Cluster.query.all())
    total_messages = sum(len(user.get_messages()) for user in User.query.all())
    total_conversations = sum(len(cluster.get_conversations()) for cluster in Cluster.query.all())
    
    clusters = Cluster.query.all()
    labels = [cluster.name for cluster in clusters]
    data = [len(cluster.get_members()) for cluster in clusters]
    
    return render_template('analytics.html', 
        total_users=total_users,
        total_clusters=total_clusters,
        total_requests=total_requests,
        total_messages=total_messages,
        total_conversations=total_conversations,
        labels=labels,
        data=data
    )
    
"""  
@app.route('/send_message', methods=['GET', 'POST'])
@login_required
def send_message():
    if session.get('user_id') != 1:
        return redirect('/home')
    
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        users = User.query.all()
        for user in users:
            msg = Message(subject, 
                          sender='noreply@clustershub.co.zw', 
                          recipients=[user.email])
            msg.html = render_template('email_message.html', 
                                       message=message, 
                                       user=user)
            mail.send(msg)
        return 'Messages sent successfully!'
    return render_template('send_message.html')
"""

@app.template_filter('linkify')
def linkify(text):
    if not text:
        return ''
    # safe to process
    text = text.replace('\n', '<br>')
    text = re.sub(r'([\w\.-]+@[\w\.-]+\.\w+)', r'<span style="color:deepSkyBlue;">\1</span>', text)
    text = re.sub(r'@(\w+)', r'<span style="color: deepSkyBlue;">@\1</span>', text)
    text = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank" style="color: deepSkyBlue">\1</a>', text)
    text = re.sub(r'#(\w+)', r'<span style="color: green;">#\1</span>', text)
    return Markup(text)
    
    
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


# BACKUP   



@app.route('/sync')
def sync():
    if not os.path.exists(DB_PATH):
        download_remote_db()
        return "Downloaded DB", 200
    
    local_ts = get_local_timestamp()
    remote_ts = get_remote_timestamp()
    if not local_ts or not remote_ts:
        return "Missing timestamp", 500
    if remote_ts > local_ts:
        download_remote_db()
        return "Downloaded newer DB", 200
    elif local_ts > remote_ts:
        upload_local_db()
        return "Uploaded newer DB", 200
    else:
        return "Already synced", 200

   
if __name__ == '__main__':
    app.run(debug=True)