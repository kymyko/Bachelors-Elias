from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange

from flask_wtf import FlaskForm


class DummyForm(FlaskForm):
    pass


class WorkingHoursForm(FlaskForm):
    pass


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = StringField('Description', validators=[DataRequired(), Length(max=255)])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('normal_user', 'Patient'),
                                                  ('psychologist', 'Psychologist')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

    name = StringField('Name (for psychologists)')
    age = IntegerField('Age (for psychologists)')
    # Set minimum age for the psychologist
    specialization = StringField('Specialization (for psychologists)')

    submit = SubmitField('Save Changes')
