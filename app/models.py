from datetime import datetime

from werkzeug.security import  generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import db
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x03
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    avatar_url = db.Column(db.String, default='/static/images/default.png')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    collections = db.relationship('Collect', backref=db.backref('collector', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def collect(self, post):
        if not self.is_collecting(post):
            c = Collect(collector=self, collection=post)
            db.session.add(c)

    def uncollect(self, post):
        c = self.collections.filter_by(post_id=post.id).first()
        if c:
            db.session.delete(c)

    def is_collecting(self, post):
        return self.collections.filter_by(post_id=post.id).first() is not None

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    body_format = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    collectors = db.relationship('Collect', backref=db.backref('collection', lazy='joined'), lazy='dynamic',
                                 cascade='all, delete-orphan')

    def is_sellected_by(self, user):
        return self.collectors.filter_by(user_id=user.id).first() is not None

class Collect(db.Model):
    __tablename__ = 'collects'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
