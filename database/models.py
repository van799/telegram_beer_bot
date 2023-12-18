from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column()
    beer: Mapped["Beer"] = relationship(back_populates='user', uselist=False)


class Beer(Base):
    __tablename__ = "beers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    photo_id: Mapped[str] = mapped_column()
    user: Mapped["User"] = relationship(back_populates="beer", uselist=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    sort_beer_id: Mapped[int] = mapped_column(ForeignKey('sortbeers.id'))

    comment: Mapped[str] = mapped_column()
    rating: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()


class SortBeer(Base):
    __tablename__ = "sortbeers"

    id: Mapped[int] = mapped_column(primary_key=True)
    title_sort_beer: Mapped[str] = mapped_column()
