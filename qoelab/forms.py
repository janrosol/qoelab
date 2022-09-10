from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from qoelab.modules import User

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


class LoginForm(FlaskForm):
    username=StringField(label='Login:', validators=[DataRequired()])
    password=PasswordField(label='Hasło:', validators=[DataRequired()])
    submit = SubmitField(label='Zaloguj się')

class Survey(FlaskForm):
    sex = StringField(label='Płeć:')
    education = StringField(label='Wykształcenie:')
    age = IntegerField(label='Wiek:')
    vision_defect = StringField(label='Wada wzroku:')
    submit = SubmitField(label='Gotowe')
    rate_1 = IntegerField(label='Ocena:', validators=[NumberRange(min=1, max=5)])
    rate_2 = IntegerField(label='Ocena:', validators=[NumberRange(min=1, max=5)])
    rate_3 = IntegerField(label='Ocena:', validators=[NumberRange(min=1, max=5)])

class Buttons(FlaskForm):
    button_next = SubmitField(label='Dalej')
    button_back = SubmitField(label='Wyjdź')
    button_start = SubmitField(label='Rozpocznij badanie')
    button_exit = SubmitField(label='Zakończ badanie')

class NASA_TLX(FlaskForm):
    q_1 = IntegerField(validators=[NumberRange(min=1, max=10)])
    q_2 = IntegerField(validators=[NumberRange(min=1, max=10)])
    q_3 = IntegerField(validators=[NumberRange(min=1, max=10)])
    q_4 = IntegerField(validators=[NumberRange(min=1, max=10)])
    q_5 = IntegerField(validators=[NumberRange(min=1, max=10)])
    q_6 = IntegerField(validators=[NumberRange(min=1, max=10)])