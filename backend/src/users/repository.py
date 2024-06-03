from core.db.repository import SyncSQLAlchemyRepository

from .models import User


class UserRepository(SyncSQLAlchemyRepository[User]):
    model = User
