from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger, select
from sqlalchemy.orm import declarative_base, as_declarative, relationship, mapped_column, Mapped, Session

# соединение машина соединений engine,
engine = create_engine('sqlite:///./test.db', echo=True)

Base = declarative_base()


class AbstractModel(Base):
    __tablename__ = "base"
    id = mapped_column(Integer, autoincrement=True, primary_key=True)


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column()
    fullname: Mapped[str] = mapped_column()
    addresses = relationship("Address", back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email_address: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user = relationship("User", back_populates="addresses")


with Session(engine) as session:
    with session.begin():
        AbstractModel.metadata.create_all(engine)
        user = User(id=1,
                    user_id=1,
                    name='lexx',
                    fullname='Dmitriev',
                    )
        session.add(user)
    with session.begin():
        result= session.execute(select(User).where(User.user_id == 1))
        user = result.scalar()
        print(user.name)