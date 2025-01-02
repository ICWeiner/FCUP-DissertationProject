from . import db

class User(db.Model):
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

    created = db.Column(
        db.DateTime,
        index = False,
        unique = False,
        nullable = False
    )

    admin = db.Column(
        db.Boolean,
        index = False,
        unique = False,
        nullable = False
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
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
        unique = True,
        nullable = False
    )

    description = db.Column(
        db.String(255),
        index = False,
        unique = False,
        nullable = False
    )

    created = db.Column(
        db.DateTime,
        index = False,
        unique = False,
        nullable = False
    )


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
        foreign_key = db.ForeignKey("user.id"),
        nullable = False
    )

    exercise_id = db.Column(
        db.Integer,
        foreign_key = db.ForeignKey("exercise.id"),
        nullable = False
    )

    created = db.Column(
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

    Status = db.Column(
        db.String(60),
        nullable = True
    )

    user = db.relationship('user', backref=db.backref('submissions', lazy=True))

    exercise = db.relationship('exercise', backref=db.backref('submissions', lazy=True))

    def __repr__(self):
        return '<Submission {}>'.format(self.id)