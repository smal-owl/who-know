from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class QuestsForm(FlaskForm):
    content = TextAreaField("Содержание", validators=[DataRequired()])
    user_id = StringField("User")
    submit = SubmitField('Отправить ответ')
