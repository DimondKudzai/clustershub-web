from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    _tablename_ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String)
    description = db.Column(db.Text)
    website = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String)
    password = db.Column(db.String)
    image = db.Column(db.String)

    skills = db.Column(db.Text)  # JSON stringified list
    clusters_count = db.Column(db.Integer)
    created_clusters = db.Column(db.Text)  # JSON stringified list
    clusters_requests = db.Column(db.Text)  # JSON stringified list
    notifications_count = db.Column(db.Integer)
    location = db.Column(db.String)

    messages = db.Column(db.Text)  # JSON stringified list of objects

    # helper methods
    def get_skills(self):
        return json.loads(self.skills or '[]')

    def get_created_clusters(self):
        return json.loads(self.created_clusters or '[]')

    def get_clusters_requests(self):
        return json.loads(self.clusters_requests or '[]')

    def get_messages(self):
        return json.loads(self.messages or '[]')


class Cluster(db.Model):
    _tablename_ = 'clusters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    target = db.Column(db.Text)
    author = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String)
    description = db.Column(db.Text)

    tags = db.Column(db.Text)       # JSON stringified list
    members = db.Column(db.Text)    # JSON stringified list
    conversations = db.Column(db.Text)  # JSON stringified list of objects
    requests = db.Column(db.Text)       # JSON stringified list of objects

    def get_tags(self):
        return json.loads(self.tags or '[]')

    def get_members(self):
        return json.loads(self.members or '[]')

    def get_conversations(self):
        return json.loads(self.conversations or '[]')

    def get_requests(self):
        return json.loads(self.requests or '[]')


class Suggestion(db.Model):
    _tablename_ = 'suggestions'

    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.Text) # JSON stringified list of objects
    
    def get_skills(self):
        return json.loads(self.skills or '[]')
    