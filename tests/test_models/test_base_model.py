"""Test the BaseModel"""
import unittest
from datetime import datetime, timedelta
from uuid import UUID
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bot.models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class TestModel(BaseModel):
    __tablename__ = "test_model"
    name = Column(String(50), nullable=False)


class TestBaseModel(unittest.TestCase):
    """Unit tests for BaseModel"""

    @classmethod
    def setUpClass(cls):
        """Set up the test database"""
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.drop_all(cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)


    def setUp(self):
        """Set up a new session for each test"""
        self.session = self.Session()


    def tearDown(self):
        """Rollback any changes after each test"""
        self.session.rollback()
        self.session.close()


    def test_id_generation(self):
        """Test if id is generated and is a valid UUID"""
        obj = TestModel(name="Sample")
        self.assertIsNotNone(obj.id)
        self.assertIsInstance(UUID(obj.id), UUID)


    def test_created_at_not_set_before_commit(self):
        """Test that created_at is None before the object is committed"""
        obj = TestModel(name="Sample")
        self.assertIsNone(obj.created_at)
        self.assertIsNone(obj.updated_at)


    def test_created_at_after_commit(self):
        """Test if created_at is correctly set after commit"""
        obj = TestModel(name="Sample")
        self.session.add(obj)
        self.session.commit()
        self.assertIsNotNone(obj.created_at)
        self.assertIsInstance(obj.created_at, datetime)


    def test_updated_at_after_commit(self):
        """Test if updated_at is correctly set after commit"""
        obj = TestModel(name="Sample")
        self.session.add(obj)
        self.session.commit()
        self.assertIsNotNone(obj.updated_at)
        self.assertIsInstance(obj.updated_at, datetime)


    def test_updated_at_changes_on_update(self):
        """Test if updated_at is modified on update"""
        obj = TestModel(name="Sample")
        self.session.add(obj)
        self.session.commit()


        original_updated_at = obj.updated_at
        obj.updated_at = datetime.utcnow() + timedelta(seconds=1)
        self.session.commit()

        self.assertNotEqual(original_updated_at, obj.updated_at)


if __name__ == "__main__":
    unittest.main()
