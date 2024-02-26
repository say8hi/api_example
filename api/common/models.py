import datetime
from typing import Annotated, Optional
from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    full_name: Mapped[str]
    registered_at: Mapped[created_at]
