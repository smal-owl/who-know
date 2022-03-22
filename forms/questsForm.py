from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class QuestsForm(FlaskForm):
    content = TextAreaField("Содержание", validators=[DataRequired()])
    news_id = TextAreaField("News")
    submit = SubmitField('Отправить ответ')