"""Populate tables with initial data

Revision ID: a35b11590718
Revises: ab9c3531c488
Create Date: 2025-03-26 18:05:06.587991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 
import datetime



# revision identifiers, used by Alembic.
revision: str = 'a35b11590718'
down_revision: Union[str, None] = 'ab9c3531c488'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    metadata = sa.MetaData()
    bind = op.get_bind()

    # Define the tables explicitly using SQLAlchemy's Table class
    user = sa.Table('user', metadata, autoload_with=bind)
    templatevm = sa.Table('templatevm', metadata, autoload_with=bind)
    exercise = sa.Table('exercise', metadata, autoload_with=bind)
    workvm = sa.Table('workvm', metadata, autoload_with=bind)
    submission = sa.Table('submission', metadata, autoload_with=bind)


    op.bulk_insert(user, 
                   [
                {
                "created_on": datetime.datetime(2023, 1, 1, 12, 0, 0),
                "username": "johndoe",
                "email": "johndoe@mail.com",
                "id": 1,
                "hashed_password": "$2b$12$Ytt6KbdiTJaB5KxleeEtUOj1.ev2Bu13Us8Kvz86.pdorVwQpbsVu",
                "last_login": datetime.datetime(2023, 5, 10, 14, 30, 0),
                "admin": True
                },
        ]
    )   

    # Insert data into the 'templatevm' table
    op.bulk_insert(templatevm,
        [
            {"created_on": datetime.datetime(2023, 1, 1, 10, 0, 0), "proxmox_id": 100, "id": 1},
        ]
    )

    # Insert data into the 'exercise' table
    op.bulk_insert(exercise,
        [
            {"created_on": datetime.datetime(2023, 1, 1, 11, 0, 0), "id": 1, "name": "Exercise 1", "description": "Description for exercise 1", "templatevm_id": 1},
        ]
    )

    # Insert data into the 'workvm' table
    op.bulk_insert(workvm,
        [
            {"created_on": datetime.datetime(2023, 1, 1, 13, 0, 0), "proxmox_id": 101, "id": 1, "user_id": 1, "templatevm_id": 1},
        ]
    )

    # Insert data into the 'submission' table
    op.bulk_insert(submission,
        [
            {"created_on": datetime.datetime(2023, 1, 1, 14, 0, 0), "id": 1, "user_id": 1, "exercise_id": 1, "workvm_id": 1, "score": 95.0, "output": "Output for submission 1", "status": "completed"},
        ]
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
