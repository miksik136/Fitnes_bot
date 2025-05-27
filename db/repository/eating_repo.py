from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Eatings


class EatingsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_eatings(self, user_id: int, calories: int, day_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                eating = Eatings(user_id=user_id, calories=calories, day_id=day_id)
                try:
                    session.add(eating)
                except:
                    return False
                return True