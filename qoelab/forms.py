from qoelab.modules import User
from flask_wtf import FlaskForm
from wtforms.validators import Email, NumberRange, Length, EqualTo, ValidationError, DataRequired 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField


#Klasa RegisterForm

class Form_Register(FlaskForm):
    def user_name_validation(self, user_check):
        user = User.query.filter_by(user_name=user_check.data).first()
        if user:
            raise ValidationError("Taki użytkownik już istnieje. Spróbuj ponownie!")
    def email_validation(self, email_check):
        email = User.query.filter_by(email=email_check).first()
        if email:
            raise ValidationError("Podany adres został już wykorzystany. Spróbuj ponownie!")

    user_name = StringField(label='Login:', validators=[Length(max=30), DataRequired()])
    email = StringField(label='Adres e-mail:', validators=[Email(), DataRequired()])
    pwd1 = PasswordField(label='Hasło:', validators=[Length(min=6), DataRequired()])
    pwd2 = PasswordField(label='Potwierdź hasło:', validators=[EqualTo('pwd1'), DataRequired()])
    save = SubmitField(label='Utwórz konto')

#Klasa LoginForm

class Form_Login(FlaskForm):
    user_name=StringField(label='Login:', validators=[DataRequired()])
    pwd=PasswordField(label='Hasło:', validators=[DataRequired()])
    save=SubmitField(label='Zaloguj się')

#Klasa TestSurvey

class TestSurvey(FlaskForm):
    sex = SelectField(label='Płeć:')
    education = SelectField(label='Wykształcenie:')
    age = SelectField(label='Wiek:')
    left_eye = SelectField(label='Lewe oko:')
    right_eye = SelectField(label='Prawe oko:')

#Klasa Buttons

class Buttons(FlaskForm):
    button_next = SubmitField(label='Dalej')
    button_back = SubmitField(label='Wyjdź bez zapisywania')
    button_exit = SubmitField(label='Zakończ badanie i zapisz')

#Klasa NASA_TLX

class NASA_TLX(FlaskForm):
    q_1 = SelectField()
    q_2 = SelectField()
    q_3 = SelectField()
    q_4 = SelectField()
    q_5 = SelectField()
    q_6 = SelectField()