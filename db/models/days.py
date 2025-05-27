from sqlalchemy import BigInteger, Column, ForeignKey

from db.base import CleanModel, BaseModel


class Days(CleanModel, BaseModel):
    __tablename__ = 'days'

    number_day = Column(BigInteger, primary_key=True, unique=False, nullable=False)
    total_calories = Column(BigInteger, nullable=True, unique=False, default=0)
    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)