from sqlmodel import Field

from src.entities.base import CommonInfoModel


class UserBase(CommonInfoModel):
    phone_number: str = Field()
    name: str | None = Field(default=None)

class User(UserBase, table=True):
    # private fields here
    pass

class UserRead(UserBase):
    pass

class UserCreate(UserBase):
    pass
