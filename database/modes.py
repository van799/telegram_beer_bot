from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(String(64))


class SortBeer(Base):
    __tablename__ = "sortbeers"

    id: Mapped[int] = mapped_column(primary_key=True)
    sort_beer: Mapped[str] = mapped_column()
    beers = relationship('Beer', back_populates='sortbeer')


class Beer(Base):
    __tablename__ = "beers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    photo_id: Mapped[str] = mapped_column()
    sort_beer_id: Mapped[str] = mapped_column(ForeignKey('sortbeers.id'))
    sort_beer = relationship("SortBeer", back_populates='beer')
    comment: Mapped[str] = mapped_column()
    rating: Mapped[str] = mapped_column()
    price: Mapped[str] = mapped_column()
