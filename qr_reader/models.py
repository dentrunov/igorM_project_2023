from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Pupils(Base):
    __tablename__ = "pupils"
    pupil_id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger(), index=True, default=0)
    pupil_name: Mapped[str] = mapped_column(String(64), index=True)
    last_visit: Mapped[int] = mapped_column(DateTime())
    last_generated_code: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    last_generated_code_date: Mapped[int] = mapped_column(DateTime())
    at_school: Mapped[bool] = mapped_column(Boolean(), default=False)

    def __repr__(self):
        return '<Pupil {}>'.format(self.pupil_name)