from sqlmodel import Session
from typing import Optional, List
from app.models import Submission, User, UserPublic, WorkVm, Exercise
from app.repositories.base import BaseRepository

class SubmissionRepository(BaseRepository):
    __entity_type__ = Submission
