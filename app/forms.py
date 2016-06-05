from flask_wtf import Form
from wtforms import StringField, validators, TextAreaField

class TweetForm(Form):
    tweet_content = TextAreaField('content', [validators.DataRequired()])
