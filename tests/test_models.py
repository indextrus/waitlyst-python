import uuid
import unittest2

from waitlyst.models import User


class UserTestCase(unittest2.TestCase):
    def setUp(self) -> None:
        self.user_id = str(uuid.uuid4())

    def test_initialization(self):
        """Test module has successfully initialized."""
        user = User()
        self.assertIsInstance(user, User)
        self.assertIsNone(user.id)
        self.assertIsNone(user.anonymous_id)

    def test_reset(self):
        """Test resetting the user."""
        user = User(anonymous_id="anon", id=self.user_id)
        self.assertEqual(user.id, self.user_id)
        self.assertEqual(user.anonymous_id, "anon")
        self.assertEqual(str(user), f"User(id={self.user_id}, anonymous_id=anon)")

        # Rest
        user.reset()
        self.assertIsNone(user.id)
        self.assertIsNone(user.anonymous_id)
