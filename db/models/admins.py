from sqlalchemy import Column, BigInteger, String

from db.base import CleanModel, BaseModel


class Admins(CleanModel, BaseModel):
    __tablename__ = 'admins'

    admin_id  = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    username = Column(String, nullable=True)