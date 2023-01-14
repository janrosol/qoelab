from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from qoelab.modules import User

#Klasa RegisterForm

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Taki użytkownik już istnieje. Spróbuj ponownie!")
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Podany adres został już wykorzystany. Spróbuj ponownie!")

    username = StringField(label='Login:', validators=[Length(min=3, max=30), DataRequired()])
    email_address = StringField(label='Adres e-mail:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Hasło:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Potwierdź hasło:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Utwórz konto')

#Klasa LoginForm

class LoginForm(FlaskForm):
    username=StringField(label='Login:', validators=[DataRequired()])
    password=PasswordField(label='Hasło:', validators=[DataRequired()])
    submit = SubmitField(label='Zaloguj się')

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