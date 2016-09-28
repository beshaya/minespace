from flask import current_app, Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def init_app(app):
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32))
    authorId = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    imageUrl = db.Column(db.String(255))
    content = db.Column(db.Text)

    def __init__(self, author, authorId, content, imageUrl="", date=None):
        self.author = author
        self.authorId = authorId
        self.content = content
        if date is None:
            date = datetime.utcnow()
        self.date = date

    def __repr__(self):
        return "<Post(author=%s content=%s)>" % (self.author, self.content)
        
if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")
