from fastapi import APIRouter, FastAPI, HTTPException
from api.common.orm import AsyncORM
from typing import List

from api.common.schemas import StatusResponse, UserBaseDTO, UserDTO, UserInDBBaseDTO, UserUpdateDTO


app = FastAPI(title="API Example")

user_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/", response_model=List[UserDTO])
async def get_users():
    users = await AsyncORM.select_all_users()
    return users


@user_router.get("/{user_id}", response_model=UserDTO)
async def get_user(user_id: int):
    user = await AsyncORM.select_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.post("/", response_model=StatusResponse)
async def create_user(user_data: UserBaseDTO):
    user_id = await AsyncORM.insert_user(user_data)
    return StatusResponse(status="ok", data={"user_id": user_id})


@user_router.put("/{user_id}", response_model=UserDTO)
async def update_user(user_id: int, user_data: UserUpdateDTO):
    user = await AsyncORM.select_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = await AsyncORM.update_user(user_id, **user_data.model_dump)
    return user


@user_router.delete("/{user_id}", response_model=StatusResponse)
async def delete_user(user_id: int):
    user = await AsyncORM.select_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await AsyncORM.delete_user(user_id)
    return StatusResponse(status="ok", data=f"User {user_id} was deleted")


app.include_router(user_router)
