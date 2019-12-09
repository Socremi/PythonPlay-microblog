from app import login
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5  # This line added in Chapter 6
# The next imports were added in Chapter 10
from time import time
import jwt
from app import app


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# The following table was added in Chapter 8 of the Flask Mega Tutorial
followers = db.Table('followers',
                     db.Column('follower_id',
                               db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id',
                               db.Integer,
                               db.ForeignKey('user.id')))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # The next line (followed) was added in Chapter 8
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # This method was added in Chapter 6
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}' \
            .format(digest, size)

    # Methods below this line for this class were added in Chapter 8
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    # This method tells SQLAlchemy how to retrieve posts from users that the
    # passed-in user has followed. It joins the followers table with the Post
    # table where the user_id associated with the post matches that of any of
    # the followed users (hence followers.c.followed_id). It filter's the
    # result to only the posts were the follower_id of the followers table
    # matches the user's own id. It is then order by the timestamp in the Post
    # table in descending order.
#    def followed_posts(self):
#        return Post.query.join(
#            followers, (followers.c.followed_id == Post.user_id)).filter(
#                followers.c.follower_id == self.id).order_by(
#                    Post.timestamp.desc())
# The above method was commented out in favour of the below method to include
# the user's own posts.
    # The folowing method works by first creating an artificial table called
    # "followed" constructed from the followers table and the posts table,
    # only taking elements where the current user is in the followers table as
    # a follower of another user (the "followed" user), using that information
    # to determine the id of the followed user (followed_id) to retrieve posts
    # for the Post table where the id == followed_id
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    #  The below methods for this class were created in chapter 10
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
