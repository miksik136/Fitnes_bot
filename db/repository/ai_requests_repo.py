from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import AiRequests


class AiRequestsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_request(self, user_id: int, user_question: str, ai_answer: str):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                request = AiRequests(user_id=user_id, user_question=user_question, ai_answer=ai_answer)
                try:
                    session.add(request)
                except:
                    return False
                return True

    async def get_request_by_user_id(self, user_id):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(AiRequests).where(AiRequests.user_id == user_id)
                query = await session.execute(sql)
                return query.scalars().one_or_none()