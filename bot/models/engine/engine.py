"""Storage API"""

import os
from dotenv import load_dotenv
from bot.models.group import Group
from bot.models.topic import Topic
from bot.models.user import User
from bot.models.user_group import UserGroup
from bot.models.base_model import Base, BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Storage:
    """Manage connections to the database"""
    __engine = None
    __session = None


    def __init__(self):
        """create engine"""
        load_dotenv()

        DB_NAME = os.getenv("DB_NAME", "practice")
        DB_ENV = os.getenv("DB_ENV", "test")
        URL = f"sqlite+pysqlite:///:memory:"

        self.__engine = create_engine(URL)

        if DB_ENV == "test":
            Base.metadata.drop_all(self.__engine)
    


    def new(self, obj):
        """Add new object to the database"""
        self.__session.add(obj)


    def all(self, cls=None):
        """query on the current database session"""
        classes = [User, Group, Topic, UserGroup]
        new_dict = {}
        for clss in classes:
            if cls is None or cls is clss:
                objs = self.__session.query(clss).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict


    def save(self):
        """Save to database"""
        self.__session.commit()


    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)


    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session


    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()


    def get(self, cls, id):
        """Retrieve an instance of cls identified by id"""
        obj = self.__session.query(cls).filter_by(id=id).first()
        return obj


    def count(self, cls=None):
        """Count the number of elements in a class or count the total
        number of elements in the db"""
        return len(self.all(cls))
