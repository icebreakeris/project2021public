"""
Form classes of the project

"""

from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm): 
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

class RegisterForm(FlaskForm): 
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    repeat = PasswordField("repeat", validators=[DataRequired(), EqualTo("password")])

class SearchForm(FlaskForm): 
    search = StringField("search", validators=[DataRequired()])

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("current_password", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    repeat = PasswordField("repeat", validators=[DataRequired(), EqualTo("password")])

class ChangeEmailForm(FlaskForm):
    email = StringField("email", validators=[DataRequired(), Email()])

class ChangeUsernameForm(FlaskForm): 
    username = StringField("username", validators=[DataRequired()])

class MultipleCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class NewsCheckboxForm(FlaskForm):
    checkboxes = MultipleCheckboxField('news_preference')
        
class TopicCheckboxForm(FlaskForm):
    checkboxes = MultipleCheckboxField("topic_preference")

class DeleteAccountForm(FlaskForm): 
    confirmation_field = StringField(validators=[DataRequired()])