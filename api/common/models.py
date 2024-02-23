import datetime
from typing import Annotated
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]

class User(Base):
    __tablename__ = 'users'

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str]
    registered_at: Mapped[str] = mapped_column(nullable=True)
