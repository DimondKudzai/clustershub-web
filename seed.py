from flask import Flask
from models import db, User, Cluster, Suggestion
from config import Config
from services.appData import get_all_users, get_all_clusters, get_suggestions


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

mock_users = get_all_users()

with app.app_context():
    db.create_all()

    for data in mock_users:
        if not User.query.filter_by(email=data["email"]).first():
            user = User(**data)
            db.session.add(user)

    db.session.commit()
    print("Mock data inserted.")
