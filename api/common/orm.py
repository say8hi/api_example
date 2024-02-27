from sqlalchemy import select, delete, update

from api.common.schemas import UserBaseDTO

from .models import User
from .database import async_session_factory


class AsyncORM:
    
    session_factory = async_session_factory
    
    @classmethod
    async def insert_user(cls, user_data: UserBaseDTO) -> None:
        async with cls.session_factory() as session:
            
            user = User(**user_data.model_dump())
            session.add(user)

            await session.flush()
            await session.commit()

            # return user.id
            # TODO: Return user_id

    @classmethod
    async def select_user(cls, user_id: int = None) -> User:
        async with cls.session_factory() as session:
            query = select(User).where(User.id == user_id) 

            result = await session.execute(query)
            user = result.scalars().first()
            return user
    
    @classmethod
    async def select_all_users(cls) -> list[User]:
        async with cls.session_factory() as session:
            query = select(User)
            result = await session.execute(query)
            users = result.scalars().all()
            return users

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
