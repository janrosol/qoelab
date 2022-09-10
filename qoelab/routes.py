from qoelab import app, plotme
from flask import render_template, redirect, url_for, flash, request
from qoelab.modules import User_Data, User
from qoelab.forms import RegisterForm, LoginForm, Buttons, Survey, NASA_TLX
from qoelab import db
from flask_login import login_user, logout_user, login_required, current_user
import pandas as pd
import plotly.express as px
import json
import plotly

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/dane')
@login_required
def data_page():
    dataset = User_Data.query.all()
    return render_template('data.html', dataset=dataset)

@app.route('/statistics')
@login_required
def statistics_page():
   return render_template('statistics.html')

@app.route('/tlx', methods=['GET', 'POST'])
@login_required
def tlx_page():
    form = NASA_TLX()
    button = Buttons()
    if button.validate_on_submit():
        if 'button_exit' in request.form:
            if not (form.q_1.data and form.q_2.data and form.q_3.data and form.q_4.data and form.q_5.data and form.q_6.data):
                flash(f'Udziel odpowiedzi na wszystkie pytania', category='info')
            else:
                user = User_Data.query.get(User_Data.query.count())
                user.q_1 = form.q_1.data
                user.q_2 = form.q_2.data
                user.q_3 = form.q_3.data
                user.q_4 = form.q_4.data
                user.q_5 = form.q_5.data
                user.q_6 = form.q_6.data
                db.session.commit()
                return redirect(url_for('home_page'))
    return render_template('tlx.html', form=form, button=button)

@app.route('/experience_1', methods=['GET', 'POST'])
@login_required
def experience_page_1():
    form = Survey()
    button = Buttons()
    if button.validate_on_submit():
        if 'button_next' in request.form:
            if not form.rate_1.data:
                flash(f'Wprowadź ocenę', category='info')
            elif(form.rate_1.data < 1 or form.rate_1.data > 5):
                flash(f'Oceń wideo w skali 1-5!', category='info')
            else:
                user = User_Data.query.get(User_Data.query.count())
                user.rate_1 = form.rate_1.data
                db.session.commit()
                return redirect(url_for('experience_page_2'))
    return render_template('experience_1.html', form=form, button=button)

@app.route('/experience_2', methods=['GET', 'POST'])
@login_required
def experience_page_2():
    form = Survey()
    button = Buttons()
    if button.validate_on_submit():
        if 'button_next' in request.form:
            if not form.rate_2.data:
                flash(f'Wprowadź ocenę', category='info')
            elif(form.rate_2.data < 1 or form.rate_2.data > 5):
                flash(f'Oceń wideo w skali 1-5!', category='info')
            else:
                user = User_Data.query.get(User_Data.query.count())
                user.rate_2 = form.rate_2.data
                db.session.commit()
                return redirect(url_for('experience_page_3'))
    return render_template('experience_2.html', form=form, button=button)

@app.route('/experience_3', methods=['GET', 'POST'])
@login_required
def experience_page_3():
    form = Survey()
    button = Buttons()
    if button.validate_on_submit():
        if 'button_next' in request.form:
            if not form.rate_3.data:
                flash(f'Wprowadź ocenę', category='info')
            elif(form.rate_3.data < 1 or form.rate_3.data > 5):
                flash(f'Oceń wideo w skali 1-5!', category='info')
            else:
                user = User_Data.query.get(User_Data.query.count())
                user.rate_3 = form.rate_3.data
                db.session.commit()
                return redirect(url_for('tlx_page'))
    return render_template('experience_3.html', form=form, button=button)

@app.route('/training_session', methods=['GET', 'POST'])
@login_required
def training_page():
    form = Survey()
    button = Buttons()
    if button.validate_on_submit():
        if 'button_next' in request.form:
            if not form.rate_1.data:
                flash(f'Wprowadź ocenę', category='info')
            elif(form.rate_1.data < 1 or form.rate_1.data > 5):
                flash(f'Oceń wideo w skali 1-5!', category='info')
            else:
                return redirect(url_for('experience_page_1'))
    return render_template('training_session.html', form=form, button=button)

@app.route('/qoe_2', methods=['GET', 'POST'])
@login_required
def qoe_2_page():
    form = Survey()
    button = Buttons()
    if button.validate_on_submit():
        if 'button_next' in request.form:
            if not (form.sex.data and form.education.data and form.age.data and form.vision_defect.data):
                flash(f'Wprowadź wszystkie dane', category='info')
            else:
                survey_info = User_Data(sex=form.sex.data,
                                      education=form.education.data,
                                      age=form.age.data,
                                      vision_defect=form.vision_defect.data
                                      )
                db.session.add(survey_info)
                db.session.commit()
                dataset = User_Data.query.all()
                return redirect(url_for('training_page'))
    return render_template('qoe_2.html', form=form, button=button)

@app.route('/qoe_1', methods=['GET', 'POST'])
@login_required
def qoe_1_page():
    form = Buttons()
    if form.validate_on_submit():
        return redirect(url_for('qoe_2_page'))
    return render_template('qoe_1.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register_page():
    id = current_user.id
    if id == 1:
        form = RegisterForm()
        if form.validate_on_submit():
            user_to_create = User(username=form.username.data,
                                  email_address=form.email_address.data,
                                  password=form.password1.data)
            db.session.add(user_to_create)
            db.session.commit()
            return redirect(url_for('data_page'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'Wystąpił błąd: {err_msg}', category='danger')
    else:
        flash(f'Nie masz uprawnień aby wyświetlać tę zawartość.', category='info')
        return redirect(url_for('home_page'))

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
            ):
            login_user(attempted_user)
            flash(f'Logowanie powiodło się! Witaj {attempted_user.username}!', category='success')
            return redirect(url_for('home_page'))
        else:
            flash(f'Nieprawidłowy login lub hasło. Spróbuj ponownie!', category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Wystąpił błąd: {err_msg}', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("Zostałeś wylogowany!", category='info')
    return redirect(url_for('login_page'))