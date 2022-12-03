import unittest2


class Client(unittest2.TestCase):
    def setUp(self) -> None:
        self.waitlyst = Waitlyst('publishableKey')


    def test_initialization(self):
        """Test module has successfully initialized."""

        self.assertTrue(hasattr(self.waitlyst, "queue"))
        self.assertTrue(hasattr(self.waitlyst, "config"))
        self.assertTrue(hasattr(self.waitlyst, "track"))
        self.assertTrue(hasattr(self.waitlyst, "identify"))
        self.assertTrue(hasattr(self.waitlyst, "page"))
        self.assertTrue(hasattr(self.waitlyst, "user"))
        self.assertTrue(hasattr(self.waitlyst, "reset"))