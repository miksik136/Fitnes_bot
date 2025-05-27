from sqlalchemy import Column, BigInteger, ForeignKey

from db.base import CleanModel, BaseModel


class Eatings(CleanModel, BaseModel):
    __tablename__ = 'eatings'

    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    calories = Column(BigInteger)
    day_id = Column(BigInteger, ForeignKey('days.id'), nullable=False)