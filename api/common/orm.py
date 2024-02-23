from sqlalchemy import select, delete, update

from .models import User
from .database import async_session_factory


class AsyncORM:
    
    session_factory = async_session_factory
    
    @classmethod
    async def insert_user(cls, username: str, full_name: str) -> User:
        async with cls.session_factory() as session:
            user = User(username=username, full_name=full_name)
            session.add(user)

            await session.flush()
            await session.commit()
            return user

    @classmethod
    async def select_user(cls, user_id: int, get_all: bool = False) -> User | list[User]:
        async with cls.session_factory() as session:
            query = select(User)
            if not get_all:
                query = query.where(User.id == user_id) 

            result = await session.execute(query)
            workers = result.scalars().all()
            return workers[0] if len(workers) == 1 else workers

    @classmethod
    async def update_user(cls, user_id: int, **kwargs) -> User:
        async with cls.session_factory() as session:
            query = update(User) \
                .where(User.id == user_id) \
                .values(**kwargs)
            
            await session.execute(query)
            await session.commit()

            return await session.get(User, user_id)
    
    @classmethod
    async def delete_user(cls, user_id: int) -> None:
        async with cls.session_factory() as session:
            query = delete(User) \
                .where(User.id == user_id)
            
            await session.execute(query)
            await session.commit()
