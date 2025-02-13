from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FieldList, FormField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
)

class HostnameForm(FlaskForm):
    hostname = StringField("Hostname", validators=[Optional()])
    commands = FieldList(StringField('Command'))
    class Meta:
        csrf = False  # Disable CSRF for nested forms

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

    hostnames = FieldList(FormField(HostnameForm))
    
    submit = SubmitField('Create')