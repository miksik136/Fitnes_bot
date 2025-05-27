from db.repository.Days_repo import DaysRepository
from db.repository.admins_repo import AdminsRepository
from db.repository.ai_requests_repo import AiRequestsRepository
from db.repository.eating_repo import EatingsRepository
from db.repository.users_repo import UsersRepository

users_repository = UsersRepository()
admins_repository = AdminsRepository()
ai_requests_repository = AiRequestsRepository()
eating_repository = EatingsRepository
days_repository = DaysRepository()

__all__ = ['users_repository', 'admins_repository', 'ai_requests_repository', 'eating_repository', 'days_repository']


