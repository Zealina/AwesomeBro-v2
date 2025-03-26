"""Group model"""
from typing import List
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from bot.models.base_model import BaseModel, Base


class Group(BaseModel, Base):
    __tablename__ = "groups"

    group_telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=False, nullable=False)


    user_groups: Mapped[List["UserGroup"]] = relationship(back_populates="group", cascade="all, delete-orphan")
    topics: Mapped[List["Topic"]] = relationship(back_populates="group", cascade="all, delete-orphan")

    
    @property
    def users(self):
        """Getter for the users and roles in a group"""
        result = []
        for user_group in self.user_groups:
            user_role = {"user": user_group.user, "role": user_group.role}
            result.append(user_role)
        return result
