"""Base Model"""

from uuid import uuid4
from datetime import datetime
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    """Methods and attributes common to all objects"""
    __abstract__ = True

    id: Mapped[str] = mapped_column(String(36), primary_key=True, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False, onupdate=datetime.utcnow)


    def __init__(self, **kwargs):
        """Ensure id is set upon instantiation"""

        super().__init__(**kwargs)
        if not kwargs.get("id"):
            self.id = str(uuid4())


    def to_dict(self):
        """Dictionary representation of a class"""
        dict_repr = {}
        for k, v in self.__dict__.items():
            if not k == "_sa_instance_state":
                dict_repr[k] = v
        return dict_repr


    def __repr__(self):
        """String representation of class"""
        string = f"[({self.__class__.__name__}.{self.id}) {self.to_dict()}]"
        return string
