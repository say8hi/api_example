from pydantic import BaseModel


class UserBaseDTO(BaseModel):
    username: str
    full_name: str


class UserCreateDTO(UserBaseDTO):
    pass


class UserUpdateDTO(UserBaseDTO):
    pass


class UserInDBBaseDTO(UserBaseDTO):
    id: int

    class Config:
        orm_mode = True


class UserDTO(UserInDBBaseDTO):
    pass