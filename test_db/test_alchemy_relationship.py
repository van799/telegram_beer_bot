from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger, select
from sqlalchemy.orm import declarative_base, as_declarative, relationship, mapped_column, Mapped, Session, \
    DeclarativeBase

# соединение машина соединений engine,
engine = create_engine('sqlite:///./test.db', echo=True)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()

    addresses: Mapped[list["Address"]] = relationship(back_populates="user", uselist=True)

    def __repr__(self) -> str:
        return f'User:{self.id=}:{self.name=}'


class Address(Base):
    __tablename__ = "addresses"

    email: Mapped[str] = mapped_column(primary_key=True)
    user: Mapped["User"] = relationship(back_populates="addresses", uselist=False)
    user_fk: Mapped[int] = mapped_column(ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f'Addresses:{self.email=}: {self.user_fk=}'


Base.metadata.create_all(engine)

session = Session(engine, expire_on_commit=True, autoflush=False)

user = User(id=1, name='lexx', age=30)
address = Address(email='test@dada.te')
address2 = Address(email='test2@dada.te')

user.addresses.append(address)
user.addresses.append(address2)

# session.add(user)
# session.commit()

users = session.scalars(select(User))
# addresses = session.scalars(select(Address)).all()


print(user)
print(user.addresses)
