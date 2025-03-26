"""User model"""

from typing import List
from sqlalchemy.orm import relationship, Mapped, mapped_column
from bot.models.base_model import BaseModel, Base
from bot.models.user_group import UserGroup


class User(BaseModel, Base):
    __tablename__ = "users"

    user_telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)

    user_groups: Mapped[List["UserGroup"]] = relationship(back_populates="user", cascade="all, delete-orphan")


    @property
    def groups(self):
        """getter to return a list with user groups and roles in each group"""
        result = []
        for user_group in self.user_groups:
            group_role = {"group": user_group.group, "role": user_group.role}
            result.append(group_role)
        return result
