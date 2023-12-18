import unittest

from database.models import Beer, User
from repository.repository_beer import RepositoryBeer
from repository.repository_user import RepositoryUser
from tests.common.test_database import TestDatabase


class TestRepositoryUser(unittest.IsolatedAsyncioTestCase):

    async def test_repository_get_all(self):
        test_database = TestDatabase()
        test_beer = Beer()
        test_user = User()

        test_user.telegram_id = 11111

        test_beer.price = 20
        test_beer.user_id = 1
        test_beer.photo_id = 1
        test_beer.rating = 10
        test_beer.name = 'test_beer'
        test_beer.sort_beer_id = 1
        test_beer.comment = 'test comment'

        await test_database.create_session()

        async with test_database.async_session() as session:
            repository_user = RepositoryUser(session)
            repository_beer = RepositoryBeer(session)

            await repository_user.add(test_user)
            await repository_beer.add(test_beer)

        async with test_database.async_session() as session:
            repository_beer = RepositoryBeer(session)
            result = await repository_beer.get_all()

        self.assertEqual(result.name, test_beer.name)
        test_database.remove_database_file()

    async def test_repository_get_all_many(self):
        test_database = TestDatabase()
        test_beer1 = Beer()
        test_beer2 = Beer()
        test_user = User()

        test_user.telegram_id = 11111
        # beer 1
        test_beer1.price = 20
        test_beer1.user_id = 1
        test_beer1.photo_id = 1
        test_beer1.rating = 10
        test_beer1.name = 'test_beer'
        test_beer1.sort_beer_id = 1
        test_beer1.comment = 'test comment'
        # beer 2
        test_beer2.price = 30
        test_beer2.user_id = 1
        test_beer2.photo_id = 2
        test_beer2.rating = 9
        test_beer2.name = 'test_beer_2'
        test_beer2.sort_beer_id = 1
        test_beer2.comment = 'test comment_2'

        await test_database.create_session()

        async with test_database.async_session() as session:
            repository_user = RepositoryUser(session)
            repository_beer = RepositoryBeer(session)

            await repository_user.add(test_user)
            await repository_beer.add(test_beer1)

        async with test_database.async_session() as session:
            repository_beer = RepositoryBeer(session)
            await repository_beer.add(test_beer2)

        async with test_database.async_session() as session:
            repository_beer = RepositoryBeer(session)
            result = await repository_beer.get_all()

        self.assertEqual(result[1].name, test_beer2.name)
        test_database.remove_database_file()
