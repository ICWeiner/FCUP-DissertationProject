from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
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
    proxmox_id = IntegerField(
        'Template VM Proxmox ID',
        validators=[
            DataRequired(),
        ]
    )
    gns3_file = FileField(
        'gns3project File',
        validators=[
            FileRequired(),
            FileAllowed(['gns3project'], 'GNS3 project files only!')
        ]
    )
    commands = TextAreaField(
        'Commands',
        validators=[
            Optional(),
        ]
    )
    
    submit = SubmitField('Create')