from quart_wtf import QuartForm
from quart_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, FieldList, FormField, SelectField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
)

class HostnameForm(QuartForm):
    hostname = SelectField("Hostname", validate_choice = False, validators = [Optional()])#validate_choice = False is used because the choices are populated dynamically
    commands = FieldList(StringField('Command'))
    class Meta:
        csrf = False  # Disable CSRF for nested forms

class CreateExerciseForm(QuartForm):
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