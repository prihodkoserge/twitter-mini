from flask_wtf import Form
from wtforms import validators, TextAreaField, FileField


class TweetForm(Form):
    tweet_content = TextAreaField('content', [validators.required()])
    attachment = FileField('attachment')