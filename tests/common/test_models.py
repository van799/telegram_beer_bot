from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from database.models import DeclarativeBase, Base


# создаем тестмодель, объекты которой будут храниться в бд
# class Base(DeclarativeBase):
#     pass


class TestCommon(Base):
    """
        Тестовая модель для тестирования репозитариев
    """
    __tablename__ = "test"
    id: Mapped[int] = mapped_column(primary_key=True)
    test_field: Mapped[int] = mapped_column()
