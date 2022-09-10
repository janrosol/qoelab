from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///qoelab.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    plec = db.Column(db.String(length=1), nullable=False)
    wyksztalcenie = db.Column(db.String(length=20), nullable=False)
    wiek = db.Column(db.Integer(), nullable=False)
    wada_wzroku = db.Column(db.String(length=20), nullable=False)
    ocena_1 = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f'Item {self.plec}'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/dane')
def data_page():
    items = Item.query.all()
    return render_template('data.html', items=items)

@app.route('/badanie')
def badanie_page():
    return render_template('admin.html')

