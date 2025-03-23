from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class UserBase(SQLModel):
    username: str = Field( unique=True, nullable=False, max_length=64)
    email: str = Field( unique=True, nullable=False, max_length=80)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    hashed_password: str = Field(nullable=False, max_length=200)
    created_on: datetime = Field(nullable=False, default=datetime.now())
    last_login: Optional[datetime] = Field(nullable=True, default=None)
    admin: bool = Field(nullable=False, default=None)

    submissions: List["Submission"] = Relationship(back_populates="user")
    workvms: List["WorkVm"] = Relationship(back_populates="user")

class UserPublic(UserBase):
    id: int

class UserCreate(UserBase):
    hashed_password: str
    admin: bool

class UserUpdate(UserBase):
    email: str | None = None
    hashed_password: str | None = None


class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    name: str = Field(nullable=False, max_length=64)
    description: str = Field(nullable=False, max_length=255)
    created_on: datetime = Field(nullable=False, default=datetime.now())
    templatevm_id: Optional[int] = Field(default=None, foreign_key="templatevm.id", nullable=True)

    submissions: List["Submission"] = Relationship(back_populates="exercise")
    templatevm: Optional["TemplateVm"] = Relationship(back_populates="exercise")  # One-to-One

class WorkVm(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    proxmox_id: int = Field(nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    templatevm_id: int = Field(foreign_key="templatevm.id", nullable=False)
    created_on: datetime = Field(nullable=False, default=datetime.now())

    submissions: List["Submission"] = Relationship(back_populates="workvm")
    user: "User" = Relationship(back_populates="workvms")
    templatevm: "TemplateVm" = Relationship(back_populates="workvms")

    class Config:
        table_constraints = [
            "UNIQUE(user_id, templatevm_id)"  # Equivalent to SQLAlchemy's UniqueConstraint
        ]

class TemplateVm(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    proxmox_id: int = Field(nullable=False)
    created_on: datetime = Field(nullable=False, default=datetime.now())

    exercise: Optional["Exercise"] = Relationship(back_populates="templatevm")  # One-to-One
    workvms: List["WorkVm"] = Relationship(back_populates="templatevm")  # One-to-Many

class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    exercise_id: int = Field(foreign_key="exercise.id", nullable=False)
    workvm_id: int = Field(foreign_key="workvm.id", nullable=False)
    created_on: datetime = Field(nullable=False, default=datetime.now())
    score: Optional[float] = Field(default=None, nullable=True)
    output: Optional[str] = Field(default=None, nullable=True, max_length=255)
    status: Optional[str] = Field(default=None, nullable=True, max_length=60)

    user: "User" = Relationship(back_populates="submissions")
    exercise: "Exercise" = Relationship(back_populates="submissions")
    workvm: "WorkVm" = Relationship(back_populates="submissions")
