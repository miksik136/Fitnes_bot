from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import DatabaseEngine
from db.models.admins import Admins


class AdminsRepository:
    def __init__(self):
        self.session_maker = DatabaseEngine().create_session()

    async def add_admin(self, admin_id: int | str, username: str):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                admin = Admins(admin_id=int(admin_id), username=username)
                try:
                    session.add(admin)
                except:
                    return False
                return True

    async def get_admin_by_admin_id(self, admin_id):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Admins).where(Admins.admin_id == admin_id)
                query = await session.execute(sql)
                return query.scalars().one_or_none()


    async def select_all_admins(self):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = select(Admins)
                query = await session.execute(sql)
                return query.scalars().all()

    async def delete_admin_by_admin_id(self, admin_id):
        async with self.session_maker() as session:
            session: AsyncSession
            async with session.begin():
                sql = delete(Admins).where(Admins.admin_id == admin_id)
                await session.execute(sql)
                await session.commit()