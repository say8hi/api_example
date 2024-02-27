from ariadne import QueryType, MutationType
from api.common.schemas import StatusResponse, UserBaseDTO
from api.common.orm import AsyncORM

query = QueryType()
mutation = MutationType()


@query.field("getUser")
async def resolve_get_user(obj, info, user_id: int):
    result = await AsyncORM.select_user(user_id)
    return result


@query.field("getAllUsers")
async def resolve_get_all_users(obj, info):
    result = await AsyncORM.select_all_users()
    return result


@mutation.field("createUser")
async def resolve_create_user(obj, info, user_data: dict):
    create_user_data = UserBaseDTO.model_validate(user_data)
    result = await AsyncORM.insert_user(create_user_data)
    return result


@mutation.field("updateUser")
async def resolve_update_user(obj, info, user_id: int, user_data: UserBaseDTO):
    update_user_data = UserBaseDTO.model_validate(user_data)
    result = await AsyncORM.update_user(user_id, **update_user_data.model_dump())
    return result


@mutation.field("deleteUser")
async def resolve_delete_user(obj, info, user_id: int):
    await AsyncORM.delete_user(user_id)
    return StatusResponse(status="ok", data=f"User {user_id} was deleted")
