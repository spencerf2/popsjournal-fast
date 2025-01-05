from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from src.entities.base import CommonInfoModel

if TYPE_CHECKING:
    from src.entities.theme import Question, Theme, ThemeUserLink


class UserBase(CommonInfoModel):
    phone_number: str = Field()
    name: str | None = Field(default=None)


class User(UserBase, table=True):
    theme_links: list["ThemeUserLink"] = Relationship(back_populates="user")
    themes_created: list["Theme"] = Relationship(back_populates="created_by")
    questions_created: list["Question"] = Relationship(back_populates="created_by")


class UserRead(UserBase):
    pass


class UserCreate(UserBase):
    pass
