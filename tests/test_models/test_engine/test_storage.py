"""Unittest for storage"""

import unittest
from bot.models.engine.engine import Storage
from bot.models.group import Group
from bot.models.topic import Topic
from bot.models.user import User
from bot.models.user_group import UserGroup

class TestStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup test database and session"""
        cls.storage = Storage()
        cls.storage.reload()

    def setUp(self):
        """Clear all tables before each test"""
        self.clear_database()

    def clear_database(self):
        """Deletes all records from tables"""
        for cls in [UserGroup, Topic, Group, User]:
            for obj in self.storage.all(cls).values():
                self.storage.delete(obj)
        self.storage.save()

    def test_database_initialization(self):
        """Test if database is initialized properly"""
        self.assertIsInstance(self.storage, Storage)

    def test_add_and_get_object(self):
        """Test adding and fetching objects"""
        user = User(user_telegram_id=1001, username="TestUser1")
        self.storage.new(user)
        self.storage.save()

        fetched_user = self.storage.get(User, user.id)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.username, "TestUser1")

    def test_get_nonexistent_object(self):
        """Test getting a nonexistent object returns None"""
        result = self.storage.get(User, 99999)
        self.assertIsNone(result)

    def test_fetch_all_objects(self):
        """Test fetching all objects of a type"""
        user1 = User(user_telegram_id=2001, username="User1")
        user2 = User(user_telegram_id=2002, username="User2")
        self.storage.new(user1)
        self.storage.new(user2)
        self.storage.save()

        all_users = self.storage.all(User)
        self.assertEqual(len(all_users), 2)

    def test_update_object(self):
        """Test updating an object"""
        user = User(user_telegram_id=3001, username="OldName")
        self.storage.new(user)
        self.storage.save()

        user.username = "NewName"
        self.storage.save()

        updated_user = self.storage.get(User, user.id)
        self.assertEqual(updated_user.username, "NewName")

    def test_delete_object(self):
        """Test deleting an object"""
        user = User(user_telegram_id=4001, username="DeleteMe")
        self.storage.new(user)
        self.storage.save()

        self.storage.delete(user)
        self.storage.save()

        deleted_user = self.storage.get(User, user.id)
        self.assertIsNone(deleted_user)

    def test_cascade_delete_group(self):
        """Test cascading delete for group -> topics, user_groups"""
        group = Group(group_telegram_id=5001, name="TestGroup")
        topic = Topic(name="TestTopic", topic_telegram_id=5555, group_id=group.id)
        user = User(user_telegram_id=6001, username="CascadeUser")
        user_group = UserGroup(user_id=user.id, group_id=group.id, role="member")

        group.topics.append(topic)
        group.user_groups.append(user_group)

        self.storage.new(group)
        self.storage.new(user)
        self.storage.save()

        group_id = group.id
        self.storage.delete(group)
        self.storage.save()

        # Ensure group and related records are deleted
        self.assertIsNone(self.storage.get(Group, group_id))
        self.assertIsNone(self.storage.get(Topic, topic.id))
        self.assertIsNone(self.storage.get(UserGroup, user_group.id))

        # Ensure user is NOT deleted (not cascade)
        self.assertIsNotNone(self.storage.get(User, user.id))

    def test_reload(self):
        """Test reloading from the database"""
        user = User(user_telegram_id=7001, username="ReloadUser")
        self.storage.new(user)
        self.storage.save()

        self.storage.reload()  # Reload session

        fetched_user = self.storage.get(User, user.id)
        self.assertIsNotNone(fetched_user)


    @classmethod
    def tearDownClass(cls):
        """Clean up"""
        cls.storage.close()

if __name__ == "__main__":
    unittest.main()
