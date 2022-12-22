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

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class User_Dataset(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    sex = db.Column(db.String())
    education = db.Column(db.String())
    age = db.Column(db.Integer())
    left_eye = db.Column(db.String())
    right_eye = db.Column(db.String())
    dl_speed_1 = db.Column(db.Float())
    dl_speed_2 = db.Column(db.Float())
    q_1 = db.Column(db.Integer())
    q_2 = db.Column(db.Integer())
    q_3 = db.Column(db.Integer())
    q_4 = db.Column(db.Integer())
    q_5 = db.Column(db.Integer())
    q_6 = db.Column(db.Integer())
    session_time = db.Column(db.Float())

class Statistics(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    tester_id = db.Column(db.Integer())
    sequence_name = db.Column(db.String())
    rate = db.Column(db.Integer())
    running_order = db.Column(db.Integer())

class Sex(db.Model):
    __tablename__ = 'Sex'
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
  
class Education(db.Model):
    __tablename__ = 'Education'
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
  
class Year(db.Model):
     __tablename__ = 'Age'
 
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.Integer())

class VisionDefect(db.Model):
     __tablename__ = 'Vision Defect'
 
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String())

class TLX(db.Model):
     __tablename__ = 'TLX Answers'
 
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.Integer())