"""Topic Model"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from bot.models.base_model import BaseModel, Base


class Topic(BaseModel, Base):
    """A group can have multiple topics"""
    __tablename__ = "topics"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    topic_telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    group_id: Mapped[str] = mapped_column(ForeignKey("groups.id"), nullable=False)

    group: Mapped["Group"] = relationship(back_populates="topics")
