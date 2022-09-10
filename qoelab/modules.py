from qoelab import db, login_manager
from qoelab import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=20), nullable=False, unique=True)
    email_address = db.Column(db.String(), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    def __repr__(self):
        return f'User_Data {self.username}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class User_Data(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sex = db.Column(db.String())
    education = db.Column(db.String())
    age = db.Column(db.Integer())
    vision_defect = db.Column(db.String())
    rate_1 = db.Column(db.Integer())
    rate_2 = db.Column(db.Integer())
    rate_3 = db.Column(db.Integer())
    q_1 = db.Column(db.Integer())
    q_2 = db.Column(db.Integer())
    q_3 = db.Column(db.Integer())
    q_4 = db.Column(db.Integer())
    q_5 = db.Column(db.Integer())
    q_6 = db.Column(db.Integer())

    def __repr__(self):
        return f'User_Data {self.plec}'