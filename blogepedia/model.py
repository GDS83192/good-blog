from blogepedia import db,login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable=False)
    email = db.Column(db.String(120),nullable=False)
    image = db.Column(db.String(20),nullable=False,default='default.png')
    password = db.Column(db.String(100),nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"Users('{self.username}','{self.email}','{self.image}')"


 
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    date_posted = db.Column(db.DateTime,nullable=False,default = datetime.utcnow)
    img_file = db.Column(db.String(20),nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
