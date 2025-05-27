from sqlalchemy import Column, BigInteger, ForeignKey, String

from db.base import CleanModel, BaseModel


class AiRequests(CleanModel, BaseModel):
    __tablename__ = 'ai_requests'

    user_id = Column(BigInteger, ForeignKey('users.user_id'), nullable=False)
    user_question = Column(String, nullable=False)
    ai_answer = Column(String, nullable=False, default='default_answer')