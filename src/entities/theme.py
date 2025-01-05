from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel

from src.entities.base import CommonInfoModel

if TYPE_CHECKING:
    from src.entities.user import User


class SnippetMetadata(SQLModel):
    content: str
    source: str
    page: int | None = None


class ThemeUserLink(CommonInfoModel, table=True):
    theme_id: UUID | None = Field(default=None, foreign_key="theme.id")
    user_id: UUID | None = Field(default=None, foreign_key="user.id")
    theme: "Theme" = Relationship(back_populates="user_links")
    user: "User" = Relationship(back_populates="theme_links")


class ThemeBase(CommonInfoModel):
    title: str = Field(default=None)
    description: str = Field(default=None)
    confidence_score: float = Field(default=None, nullable=True)
    supporting_snippets: list[SnippetMetadata] = Field(default=None, sa_type=JSON)
    created_by_id: UUID | None = Field(default=None, foreign_key="user.id")


class Theme(ThemeBase, table=True):
    created_by: Optional["User"] = Relationship(back_populates="themes_created")
    user_links: list["ThemeUserLink"] = Relationship(back_populates="theme")
    questions: list["Question"] = Relationship(back_populates="theme")


class QuestionBase(CommonInfoModel):
    theme_id: UUID | None = Field(default=None, foreign_key="theme.id")
    text: str = Field(default=None)
    confidence_score: float = Field(default=None, nullable=True)
    supporting_snippets: list[SnippetMetadata] = Field(default=None, sa_type=JSON)
    created_by_id: UUID | None = Field(default=None, foreign_key="user.id")


class Question(QuestionBase, table=True):
    theme: Optional["Theme"] = Relationship(back_populates="questions")
    created_by: Optional["User"] = Relationship(back_populates="questions_created")
