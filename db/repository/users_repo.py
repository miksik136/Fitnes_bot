from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models import Users


class UsersRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_user(self, user_id: int, username: str):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                user = Users(user_id=user_id, username=username)
                try:
                    session.add(user)
                except:
                    return False
                return True

    async def get_user_by_user_id(self, user_id):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Users).where(Users.user_id == user_id)
                query = await session.execute(sql)
                return query.scalars().one_or_none()

    async def update_thread_id_by_user_id(self, user_id: int, thread_id: str):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = update(Users).values({Users.ai_thread_id: thread_id}).where(Users.user_id == user_id)
                await session.execute(sql)
                await session.commit()

    async def update_time_notification_by_user_id(self, user_id: int, new_time: str):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = update(Users).values({Users.time_notification: new_time}).where(Users.user_id == user_id)
                await session.execute(sql)
                await session.commit()

    async def select_all_users(self):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Users)
                query = await session.execute(sql)
                return query.scalars().all()