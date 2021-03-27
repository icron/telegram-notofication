from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class KeywordForm(FlaskForm):
    channels = StringField('Channels', validators=[DataRequired(), Length(max=1024)])
    keywords = StringField('Keywords', validators=[DataRequired(), Length(max=1024)])

