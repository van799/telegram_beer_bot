from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger, select, Table, MetaData, insert
from sqlalchemy.orm import declarative_base, as_declarative, relationship, mapped_column, Mapped, Session

# соединение машина соединений engine,
engine = create_engine('sqlite:///./test.db', echo=True)

Base = declarative_base()

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("name", String(30)),
    Column("fullname", String)
)

address_table = Table(
    "addresses",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, autoincrement=True),
    Column("email_address", String(30)),
    Column("user_id", ForeignKey('users.id')))

metadata.create_all(engine)

stnt = insert(user_table).values(name='Test', fullname='Test text')
stmt_two = insert(user_table)

with engine.begin() as conn:
    result = conn.execute(stmt_two,
                          [
                              {
                                  "name": 'TEst1',
                                  "fullname": "test_fullname1"
                              },
                              {
                                  "name": 'TEst2',
                                  "fullname": "test_fullname2"
                              },
                              {
                                  "name": 'TEst3',
                                  "fullname": "test_fullname3"
                              }
                          ])

with engine.begin() as conn:
    result = conn.execute(select(user_table).where(user_table.c.name == 'TEst1'))
    print(result.all())
