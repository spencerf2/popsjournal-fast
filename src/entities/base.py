from datetime import datetime, timezone

from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4

class CommonInfoModel(SQLModel):
    id: UUID = Field(
        primary_key=True,
        default_factory=uuid4,
        nullable=False,
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
