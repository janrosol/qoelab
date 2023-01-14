from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#URI z lokalizacją bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qoelab.db'

#Tajny klucz do zabezpieczeń
app.config['SECRET_KEY'] = 'e78257a7691c942e5e409a49'

#Obiekty niezbędne do działania aplikacji
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#Import modułu routes
from qoelab import routes
