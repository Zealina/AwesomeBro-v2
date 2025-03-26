"""Many to many relationship between group and user"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from bot.models.base_model import BaseModel, Base


class UserGroup(BaseModel, Base):
    """Relates the user and group tables in many-to-many"""
    __tablename__ = "user_groups"

    group_id: Mapped[str] = mapped_column(ForeignKey("groups.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    role: Mapped[str] = mapped_column(default="member")

    user: Mapped["User"] = relationship(back_populates="user_groups")
    group: Mapped["Group"] = relationship(back_populates="user_groups")
