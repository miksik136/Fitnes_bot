import datetime

from sqlalchemy import Column, BigInteger, String, Time, func

from db.base import CleanModel, BaseModel


class Users(CleanModel, BaseModel):
    __tablename__ = 'users'

    user_id  = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=True)
    ai_thread_id = Column(String, nullable=True, unique=True)
    time_notification = Column(Time, unique=False, nullable=False, default=datetime.datetime.now().time())