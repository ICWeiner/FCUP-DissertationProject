from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FileField
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
        'Body Text',
        validators=[
            DataRequired(),
        ]
    )
    templatevm_proxmox_id = IntegerField(
        'Template VM Proxmox ID',
        validators=[
            DataRequired(),
        ]
    )
    gns3_file = FileField(
        'GNS3 File',
        validators=[
            Optional(),
        ]
    )
    commands = TextAreaField(
        'Commands',
        validators=[
            Optional(),
        ]
    )
    
    submit = SubmitField('Create')