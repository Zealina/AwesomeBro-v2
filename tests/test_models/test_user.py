"""Test User Model"""

import unittest
from sqlalchemy.exc import IntegrityError
from bot.models.user import User
from bot.models.group import Group
from bot.models.topic import Topic
from bot.models.user_group import UserGroup
from bot.models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestUserModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test database"""
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.drop_all(cls.engine)
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """Start a new session for each test"""
        self.session = self.Session()

    def tearDown(self):
        """Rollback transactions and close session"""
        self.session.rollback()
        self.session.close()

    def test_create_user(self):
        """Test creating a user"""
        user = User(user_telegram_id=12345, username="testuser")
        self.session.add(user)
        self.session.commit()
        retrieved_user = self.session.get(User, user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")

    def test_unique_user_telegram_id(self):
        """Test uniqueness constraint on user_telegram_id"""
        user1 = User(user_telegram_id=12345, username="user1")
        user2 = User(user_telegram_id=12345, username="user2")
        self.session.add(user1)
        self.session.commit()

        print("Before adding to session")
        self.session.add(user2)
        print("after adding to session")
        with self.assertRaises(IntegrityError):
            print("Into the Context manager")
            self.session.commit()

    def test_unique_username(self):
        """Test uniqueness constraint on username"""
        user1 = User(user_telegram_id=11111, username="uniqueuser")
        user2 = User(user_telegram_id=22222, username="uniqueuser")
        self.session.add(user1)
        self.session.commit()

        self.session.add(user2)
        with self.assertRaises(IntegrityError):
            self.session.commit()

    def test_user_groups_relationship(self):
        """Test user and user_groups relationship"""
        user = User(user_telegram_id=67890, username="user_with_groups")
        group1 = UserGroup(user=user, group="Group1", role="Admin")
        group2 = UserGroup(user=user, group="Group2", role="Member")
        self.session.add_all([user, group1, group2])
        self.session.commit()

        retrieved_user = self.session.get(User, user.id)
        self.assertEqual(len(retrieved_user.user_groups), 2)

    def test_groups_property(self):
        """Test the groups property returns correct structure"""
        user = User(user_telegram_id=98765, username="groupuser")
        group1 = UserGroup(user=user, group="StudyGroup", role="Moderator")
        group2 = UserGroup(user=user, group="WorkGroup", role="Member")
        self.session.add_all([user, group1, group2])
        self.session.commit()

        expected_groups = [
            {"group": "StudyGroup", "role": "Moderator"},
            {"group": "WorkGroup", "role": "Member"}
        ]
        self.assertEqual(user.groups, expected_groups)
