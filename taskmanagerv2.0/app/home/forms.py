

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError,SelectField
from wtforms.validators import DataRequired, Email, EqualTo


class TaskForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices=[('C', 'Created'),
                                            ('P', 'In progress'), ('D', 'Deleted')])
    submit = SubmitField('Submit')