from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        unique = True
    )

    username = db.Column(
        db.String(64),
        index = False,
        unique = True,
        nullable = False
    )

    email = db.Column(
        db.String(80),
        index = True,
        unique = True,
        nullable = False
    )

    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
	)

    created_on = db.Column(
        db.DateTime,
        index = False,
        unique = False,
        nullable = False
    )

    last_login = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )

    admin = db.Column(
        db.Boolean,
        index = False,
        unique = False,
        nullable = False,
        default = False
    )

    submissions  = db.relationship('Submission', backref='user')

    workvms  = db.relationship('WorkVm', backref='user')

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class WorkVm(db.Model):
    __tablename__ = 'workvm'

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique = True
    )

    proxmox_id = db.Column(
        db.Integer,
        #unique = True,
        nullable = False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable = False
    )

    templatevm_id = db.Column(
        db.Integer,
        db.ForeignKey("templatevm.id"),
        nullable = False
    )

    created_on = db.Column(
        db.DateTime,
        index = False,
        unique = False,
        nullable = False
    )

    #db.UniqueConstraint('user_id', 'templatevm_id')#Disallow duplicate user/templatevm(exercise) combos 

    submissions  = db.relationship('Submission', backref='workvm')


class TemplateVm(db.Model):
    __tablename__ = 'templatevm'

    id = db.Column(
        db.Integer,
        primary_key=True,
        unique = True
    )

    proxmox_id = db.Column(
        db.Integer,
        #unique = True,TODO:Reenable this later
        nullable = False
    )

    created_on = db.Column(
        db.DateTime,
        index = False,
        unique = False,
        nullable = False
    )

    exercise = db.relationship('Exercise', backref='templatevm', lazy=True, uselist=False)#uselist = false for one-to-one relation

    workvms  = db.relationship('WorkVm', backref='templatevm')
    
class Exercise(db.Model):
    __tablename__ = 'exercise'
    
    id = db.Column(
        db.Integer,
        primary_key=True,
        unique = True
    )

    name = db.Column(
        db.String(64),
        index = False,
        #unique = True,TODO:REENABLE THIS LATER
        nullable = False
    )

    description = db.Column(
        db.String(255),
        index = False,
        unique = False,
        nullable = False
    )

    created_on = db.Column(
        db.DateTime,
        index = False,
        unique = False,
        nullable = False
    )

    templatevm_id = db.Column(
        db.Integer,
        db.ForeignKey("templatevm.id"),
        nullable = True
    )

    submissions  = db.relationship('Submission', backref='exercise')


    def __repr__(self):
        return '<Exercise {}>'.format(self.name)
    
class Submission(db.Model):
    __tablename__ = 'submission'
    
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable = False
    )

    exercise_id = db.Column(
        db.Integer,
        db.ForeignKey("exercise.id"),
        nullable = False
    )

    workvm_id = db.Column(
        db.Integer,
        db.ForeignKey("workvm.id"),
        nullable = False
    )

    created_on = db.Column(
        db.DateTime,
        index = False,
        unique = False,
        nullable = False
    )

    score = db.Column(
        db.Float,
        nullable = True
    )

    output = db.Column(
        db.String(255),
        nullable = True
    )

    status = db.Column(
        db.String(60),
        nullable = True
    )

    def __repr__(self):
        return '<Submission {}>'.format(self.id)