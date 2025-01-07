from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional
)



class CreateExerciseForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            DataRequired(),
        ]
    )
    body = TextAreaField(
        'Body',
        validators=[
            DataRequired(),
        ]
    )
    
    submit = SubmitField('Create')