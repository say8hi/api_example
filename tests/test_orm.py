import asyncio
import pytest
from sqlalchemy import text
from api.common.orm import AsyncORM
from api.common.database import init_db
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, async_scoped_session

from api.common.schemas import UserBaseDTO


def orm_test_decorator(func):

    async def wrapper(*args, **kwargs):

        def get_current_task():
            try:
                return asyncio.current_task()
            except RuntimeError:
                return None
            
        async_engine_test = create_async_engine("sqlite+aiosqlite:///:memory:")  # TODO: replace test sqlite with postgresql
        async_session_factory_test = async_scoped_session(
            async_sessionmaker(async_engine_test, expire_on_commit=False),
            scopefunc=get_current_task
        )
        AsyncORM.session_factory = async_session_factory_test
        await init_db(async_engine_test)
        
        result = await func(*args, **kwargs)
        
        async with async_session_factory_test() as session:
            await session.execute(text("DROP TABLE IF EXISTS users"))
        
        return result
    
    return wrapper

@pytest.mark.asyncio
@orm_test_decorator
async def test_insert_user():
    user_id = await AsyncORM.insert_user(UserBaseDTO(username="testuser", full_name="Test User"))

    user = await AsyncORM.select_user(user_id)

    assert user is not None
    assert user.id == user_id
    assert user.username == "testuser"
    assert user.full_name == "Test User"



@pytest.mark.asyncio
@orm_test_decorator
async def test_update_user():
    user_id = await AsyncORM.insert_user(UserBaseDTO(username="testuser", full_name="Test User"))

    user_from_db = await AsyncORM.update_user(
        user_id,
        username="new_test_username",
        full_name="new_test_full_name"
    )

    assert user_from_db is not None
    assert user_from_db.id == user_id
    assert user_from_db.username == "new_test_username"
    assert user_from_db.full_name == "new_test_full_name"


@pytest.mark.asyncio
@orm_test_decorator
async def test_delete_user():
    user_id = await AsyncORM.insert_user(UserBaseDTO(username="testuser", full_name="Test User"))

    await AsyncORM.delete_user(user_id)

    user_from_db = await AsyncORM.select_user(user_id)

    assert not user_from_db
