from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from services.appData import get_all_users, get_all_clusters, get_suggestions



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clusters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String)
    description = db.Column(db.Text)
    website = db.Column(db.String)
    second_website = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    confirm_email = db.Column(db.Text)
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

    def get_skills(self):
        return json.loads(self.skills or '[]')

    def get_created_clusters(self):
        return json.loads(self.created_clusters or '[]')

    def get_clusters_requests(self):
        return json.loads(self.clusters_requests or '[]')

    def get_messages(self):
        return json.loads(self.messages or '[]')

    def set_skills(self, skills):
        self.skills = json.dumps(skills)

    def set_created_clusters(self, clusters):
        self.created_clusters = json.dumps(clusters)

    def set_clusters_requests(self, requests):
        self.clusters_requests = json.dumps(requests)

    def set_messages(self, messages):
        self.messages = json.dumps(messages)

class Cluster(db.Model):
    __tablename__ = 'clusters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    target = db.Column(db.Text)
    status = db.Column(db.Text)
    author = db.Column(db.String)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String)
    description = db.Column(db.Text)
    tags = db.Column(db.Text)  # JSON stringified list
    members = db.Column(db.Text)  # JSON stringified list
    conversations = db.Column(db.Text)  # JSON stringified list of objects
    requests = db.Column(db.Text)  # JSON stringified list of objects

    def get_tags(self):
        return json.loads(self.tags or '[]')

    def get_members(self):
        return json.loads(self.members or '[]')

    def get_conversations(self):
        return json.loads(self.conversations or '[]')

    def get_requests(self):
        return json.loads(self.requests or '[]')

    def set_tags(self, tags):
        self.tags = json.dumps(tags)

    def set_members(self, members):
        self.members = json.dumps(members)

    def set_conversations(self, conversations):
        self.conversations = json.dumps(conversations)

    def set_requests(self, requests):
        self.requests = json.dumps(requests)

class Suggestion(db.Model):
    __tablename__ = 'suggestions'
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.Text)  # JSON stringified list

    def get_skills(self):
        return json.loads(self.skills or '[]')

    def set_skills(self, skills):
        self.skills = json.dumps(skills)


def seed_users():
    users = get_all_users()
    for user_data in users:
        if not User.query.filter_by(email=user_data["email"]).first():
            user = User(
                name=user_data["name"],
                full_name=user_data["full_name"],
                description=user_data["description"],
                website=user_data["website"],
                second_website=user_data["second_website"],
                email=user_data["email"],
                confirm_email=user_data["confirm_email"],
                phone=user_data["phone"],
                password=user_data["password"],
                image=user_data["image"],
                skills=json.dumps(user_data["skills"]),
                clusters_count=user_data["clusters_count"],
                created_clusters=json.dumps(user_data["created_clusters"]),
                clusters_requests=json.dumps(user_data["clusters_requests"]),
                notifications_count=user_data["notifications_count"],
                location=user_data["location"],
                messages=json.dumps(user_data["messages"])
            )
            db.session.add(user)
    db.session.commit()
    

def seed_clusters():
    clusters = get_all_clusters()
    for cluster_data in clusters:
        if not Cluster.query.filter_by(id=cluster_data["id"]).first():
            cluster = Cluster(
                id=cluster_data["id"],
                name=cluster_data["name"],
                target=cluster_data["target"],
                status=cluster_data["status"],
                author=cluster_data["author"],
                created=datetime.strptime(cluster_data["created"], "%Y-%m-%dT%H:%M:%SZ"),
                location=cluster_data["location"],
                description=cluster_data["description"],
                tags=json.dumps(cluster_data["tags"]),
                members=json.dumps(cluster_data["members"]),
                conversations=json.dumps(cluster_data["conversations"]),
                requests=json.dumps(cluster_data["requests"])
            )
            db.session.add(cluster)
    db.session.commit()
    
def seed_suggestions():
    new_skills = get_suggestions()
    existing_suggestion = Suggestion.query.first()
    if existing_suggestion:
        existing_skills = existing_suggestion.get_skills()
        updated_skills = list(set(existing_skills + new_skills))
        existing_suggestion.set_skills(updated_skills)
    else:
        suggestion = Suggestion()
        suggestion.set_skills(new_skills)
        db.session.add(suggestion)
    db.session.commit()

with app.app_context():
    db.create_all()
    seed_users()
    seed_clusters()
    seed_suggestions()

if __name__ == '__main__':
    app.run(debug=True)