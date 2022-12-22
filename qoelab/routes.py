from qoelab import app, db
from flask import render_template, redirect, url_for, flash, request
from qoelab.modules import User, Sex, Education, Year, VisionDefect, User_Dataset, TLX, Statistics
from qoelab.forms import RegisterForm, LoginForm, Buttons, NASA_TLX, TestSurvey
from flask_login import login_user, logout_user, login_required, current_user
import speedtest, time, json, threading, ast, os
import pandas as pd

#Zmienne globalne
time_data=[0,0]
i=0

#Pomiary przepustowosci lacza
def dl_speed_test_1():
    download_speed = round(speedtest.Speedtest().download()/1024/1024, 2)
    user = User_Dataset.query.get(User_Dataset.query.count())
    user.dl_speed_1 = download_speed
    db.session.commit()

def dl_speed_test_2():
    download_speed = round(speedtest.Speedtest().download()/1024/1024, 2)
    user = User_Dataset.query.get(User_Dataset.query.count())
    user.dl_speed_2 = download_speed
    db.session.commit()

#Strona glowna
@app.route('/')
@app.route('/home')
def home_page():
    if time_data[0] != 0:
        time_data[1] = time.time()
        session_time = round(time_data[1] - time_data[0], 2)
        user = User_Dataset.query.get(User_Dataset.query.count())
        user.session_time = session_time
        db.session.commit()
        time_data[0] = 0
    return render_template('home.html')

#Wstep
@app.route('/qoe_1', methods=['GET', 'POST'])
@login_required
def qoe_1_page():
    form = Buttons()
    if form.validate_on_submit():
        time_data[0] = time.time()
        return redirect(url_for('qoe_2_page'))
    return render_template('qoe_1.html', form=form)

#Ankieta
@app.route('/qoe_2', methods=['GET', 'POST'])
@login_required
def qoe_2_page():
    form = TestSurvey()
    form.sex.choices = [(sex.id, sex.name) for sex in Sex.query.all()]
    form.education.choices = [(ed.id, ed.name) for ed in Education.query.all()]
    form.age.choices = [(age.id, age.name) for age in Year.query.all()]
    form.left_eye.choices = [(item.id, item.name) for item in VisionDefect.query.all()]
    form.right_eye.choices = [(item.id, item.name) for item in VisionDefect.query.all()]
    button = Buttons()
    if button.validate_on_submit():
        if 'button_next' in request.form:
            if request.method == 'POST':
                sex = Sex.query.filter_by(id=form.sex.data).first()
                education = Education.query.filter_by(id=form.education.data).first()
                age = Year.query.filter_by(id=form.age.data).first()
                left_eye = VisionDefect.query.filter_by(id=form.left_eye.data).first()
                right_eye = VisionDefect.query.filter_by(id=form.right_eye.data).first()
                survey_info = User_Dataset(sex=sex.name,education=education.name,
                                            age=age.name,left_eye=left_eye.name,
                                            right_eye=right_eye.name)
                db.session.add(survey_info)
                db.session.commit()
                shuffled_df = pd.read_csv('sequences.csv').sample(frac=1)
                shuffled_df.to_csv('shuffled_data.csv', index=False)
            return redirect(url_for('training_page'))
    return render_template('qoe_2.html', form=form, button=button)

#Sesja treningowa
@app.route('/training_session', methods=['GET', 'POST'])
@login_required
def training_page():
    ds1 = threading.Thread(target=dl_speed_test_1)
    ds1.start()
    if request.method == 'POST':
        return redirect(url_for('experience_page'))
    return render_template('training_session.html')

#Sekwencja z filmami
@app.route('/experience', methods=['GET', 'POST'])
@login_required
def experience_page():
    global i
    sequences_number = len(pd.read_csv('sequences.csv'))
    print(sequences_number)
    links = pd.read_csv('shuffled_data.csv').iloc[:,2:3].values
    titles = pd.read_csv('shuffled_data.csv').iloc[:,1:2].values
    links_new = []
    titles_new = []
    for element in links:
        links_new.append(str(element).lstrip("['").rstrip("]'"))
    for element in titles:
        titles_new.append(str(element).lstrip("['").rstrip("]'"))
    if request.method == 'POST':
        rating = request.form.get('rate_button')
        stats = Statistics(tester_id=User_Dataset.query.get(User_Dataset.query.count()).id,
                           sequence_name=titles_new[i-1],
                           rate=rating,
                           running_order=i)
        db.session.add(stats)
        db.session.commit()
        return redirect(url_for('experience_page'))
    if(i == sequences_number):
        return redirect(url_for('tlx_page'))
    else:
        i+=1
    return render_template('experience.html', listoflinks=links_new[i-1], i=i)

#Ankieta koncowa
@app.route('/tlx', methods=['GET', 'POST'])
@login_required
def tlx_page():
    global i
    if i != 0:
        i = 0
    ds2 = threading.Thread(target=dl_speed_test_2)
    ds2.start()
    form = NASA_TLX()
    form.q_1.choices = [(q.id, q.name) for q in TLX.query.all()]
    form.q_2.choices = [(q.id, q.name) for q in TLX.query.all()]
    form.q_3.choices = [(q.id, q.name) for q in TLX.query.all()]
    form.q_4.choices = [(q.id, q.name) for q in TLX.query.all()]
    form.q_5.choices = [(q.id, q.name) for q in TLX.query.all()]
    form.q_6.choices = [(q.id, q.name) for q in TLX.query.all()]
    button = Buttons()
    if button.validate_on_submit():
        if 'button_exit' in request.form:
            if request.method == 'POST':
                q_1 = TLX.query.filter_by(id=form.q_1.data).first()
                q_2 = TLX.query.filter_by(id=form.q_2.data).first()
                q_3 = TLX.query.filter_by(id=form.q_3.data).first()
                q_4 = TLX.query.filter_by(id=form.q_4.data).first()
                q_5 = TLX.query.filter_by(id=form.q_5.data).first()
                q_6 = TLX.query.filter_by(id=form.q_6.data).first()
                rates = User_Dataset.query.get(User_Dataset.query.count())
                rates.q_1 = q_1.name
                rates.q_2 = q_2.name
                rates.q_3 = q_3.name
                rates.q_4 = q_4.name
                rates.q_5 = q_5.name
                rates.q_6 = q_6.name
                db.session.commit()
                return redirect(url_for('home_page'))
        if 'button_back' in request.form:
                return redirect(url_for('home_page'))
    return render_template('tlx.html', form=form, button=button)

#Dane z ankiety wstepnej
@app.route('/dane')
@login_required
def data_page():
    dataset = User_Dataset.query.all()
    return render_template('data.html', dataset=dataset)

#Dane z oceniania sekwencji
@app.route('/statistics')
@login_required
def statistics_page():
    dataset = Statistics.query.all()
    return render_template('statistics.html', dataset=dataset)


#Rejestracja nowego uzytkownika
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

#Logowanie
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

#Wylogowanie
@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash("Zostałeś wylogowany!", category='info')
    return redirect(url_for('login_page'))