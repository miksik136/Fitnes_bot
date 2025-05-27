from sqlalchemy import Update, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Days


class DaysRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_days(self, last_number_day: int, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                day = Days(number_day=last_number_day, user_id=user_id)
                try:
                    session.add(day)
                except:
                    return False
                return True

    async def update_total_calories(self, number_day: int, user_id: int, new_calories: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = Update(Days).values({Days.total_calories: Days.total_calories + new_calories}).where(Days.user_id == user_id and Days.number_day == number_day)
                await session.execute(sql)
                await session.commit()

    async def get_all_days_user_id(self, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Days).where(Days.user_id == user_id)
                query = await session.execute(sql)
                return query.scalars().all()

    async def get_all_day_by_number(self, number: int, user_id: int):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Days).where(and_(Days.number_day == number,
                                              Days.user_id == user_id))
                query = await session.execute(sql)
                return query.scalars().one_or_none()