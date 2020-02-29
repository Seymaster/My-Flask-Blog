from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,InputRequired

class CommentForm(FlaskForm):
    body = TextAreaField('Body',validators=[InputRequired()])
    submit  = SubmitField('Post')