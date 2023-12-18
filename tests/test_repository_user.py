import unittest

from database.models import User
from repository.repository_user import RepositoryUser
from tests.common.test_database import TestDatabase


class TestRepositoryUser(unittest.IsolatedAsyncioTestCase):

    async def test_repository_get_by_telegram_id(self):
        test_database = TestDatabase()
        test_user = User()
        test_user.telegram_id = 11111111

        await test_database.create_session()

        async with test_database.async_session() as session:
            repository_user = RepositoryUser(session)
            await repository_user.add(test_user)

        async with test_database.async_session() as session:
            repository_user = RepositoryUser(session)
            result = await repository_user.get_by_telegram_id(test_user.telegram_id)

        self.assertEqual(result.telegram_id, test_user.telegram_id)
        test_database.remove_database_file()
