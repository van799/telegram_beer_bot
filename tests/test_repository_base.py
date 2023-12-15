import unittest

from tests.common.test_database import TestDatabase
from tests.common.test_models import TestCommon
from tests.common.test_repository import TestRepository


class TestRepositoryBase(unittest.IsolatedAsyncioTestCase):

    async def test_repository_add(self):
        test_database = TestDatabase()
        test_common = TestCommon()
        test_common.test_str = 'test'

        await test_database.create_session()

        async with test_database.async_session() as session:
            repository = TestRepository(session)
            await repository.add(test_common)

        async with test_database.async_session() as session:
            result = await session.get(TestCommon, 1)

        self.assertEqual(result.test_str, test_common.test_str)
        test_database.remove_database_file()
