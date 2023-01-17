from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#URI z lokalizacją bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qoelab.db'

#Tajny klucz do zabezpieczeń
app.config['SECRET_KEY'] = 'e78257a7691c942e5e409a49'

#Obiekty niezbędne do działania aplikacji
login_manager = LoginManager(app) #Logowanie
bcrypt = Bcrypt(app) #Szyfrowanie hasła
db = SQLAlchemy(app) #Baza danych

#Import modułu routes
from qoelab import routes
