import sqlalchemy as sa
from . import db
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from quart_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column( primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(200), nullable=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=sa.func.now(), server_default=sa.FetchedValue(),)
    last_login: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    admin: Mapped[bool] = mapped_column( default=False, nullable=False)


    submissions: Mapped["Submission"] = relationship('Submission', backref='user')
    workvms: Mapped["WorkVm"] = relationship('WorkVm', backref='user')

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

    id: Mapped[int] = mapped_column( primary_key=True, unique=True)
    proxmox_id: Mapped[int] = mapped_column( nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    templatevm_id: Mapped[int] = mapped_column( ForeignKey("templatevm.id"), nullable=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=sa.func.now(), server_default=sa.FetchedValue(),)

    submissions: Mapped["Submission"] = relationship('Submission', backref='workvm')

class TemplateVm(db.Model):
    __tablename__ = 'templatevm'

    id: Mapped[int] = mapped_column( primary_key=True, unique=True)
    proxmox_id: Mapped[int] = mapped_column( nullable=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=sa.func.now(), server_default=sa.FetchedValue(),)

    exercise: Mapped["Exercise"] = relationship('Exercise', backref='templatevm', lazy=True, uselist=False)  # uselist=False for one-to-one relation
    workvms: Mapped["WorkVm"] = relationship('WorkVm', backref='templatevm')
    

class Exercise(db.Model):
    __tablename__ = 'exercise'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    created_on: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=sa.func.now(), server_default=sa.FetchedValue(),)
    templatevm_id: Mapped[int] = mapped_column(ForeignKey("templatevm.id"), nullable=True) #nullable=True because templatevm id is not defined at exercise creation time

    submissions: Mapped["Submission"] = relationship('Submission', backref='exercise')

    def __repr__(self):
        return f'<Exercise {self.name}>'
    
class Submission(db.Model):
    __tablename__ = 'submission'
    
    id: Mapped[int] = mapped_column( primary_key=True )
    user_id: Mapped[int] = mapped_column( ForeignKey("user.id"), nullable=False )
    exercise_id: Mapped[int] = mapped_column( ForeignKey("exercise.id"), nullable=False )
    workvm_id: Mapped[int] = mapped_column( ForeignKey("workvm.id"), nullable=False )
    created_on: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=sa.func.now(), server_default=sa.FetchedValue(),)
    score: Mapped[float] = mapped_column( nullable=True )
    output: Mapped[str] = mapped_column( String(255), nullable=True )
    status: Mapped[str] = mapped_column( String(60), nullable=True )

    def __repr__(self):
        return f'<Submission {self.id}>'
    
