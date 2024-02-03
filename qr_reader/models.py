from sqlalchemy import String, BigInteger, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import datetime
class Base(DeclarativeBase):
    pass

class Pupils(Base):
    """ Таблица БД учеников"""
    __tablename__ = "pupils"
    pupil_id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger(), index=True, default=0)
    pupil_name: Mapped[str] = mapped_column(String(64), index=True)
    last_visit: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=None)
    out_time: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=None)
    last_generated_code: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    last_generated_code_date: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=None)
    at_school: Mapped[bool] = mapped_column(Boolean(), default=False)

    def __repr__(self):
        return '<Pupil {}>'.format(self.pupil_name)
    
    def change_time_in(self, t):
        self.last_visit = t

    def change_time_out(self, t):
        self.out_time = t
        
class NewUsers(Base):
    """ Таблица новых пользователей бота для просмотра TG ID"""
    __tablename__ = "new_users" 
    new_user_id: Mapped[int] = mapped_column(primary_key=True)
    new_user_name: Mapped[str] = mapped_column(String(64), index=True)
    new_user_tg_id: Mapped[int] = mapped_column(BigInteger(), index=True, default=0)
    new_user_datetime: Mapped[datetime.datetime] = mapped_column(DateTime(), server_default=None)

    def __repr__(self):
            return '<NewUser {}>'.format(self.new_user_name)