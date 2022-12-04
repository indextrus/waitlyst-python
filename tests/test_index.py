import uuid
import unittest2

from unittest.mock import patch

from waitlyst.events import TrackEvent, PageEvent
from waitlyst.index import Waitlyst
from waitlyst.models import User
from tests.mocks.base import MockHttpClient

mockClient = MockHttpClient()


class IndexTestCase(unittest2.TestCase):
    def setUp(self) -> None:
        self.user_id = str(uuid.uuid4())
        self.waitlyst = Waitlyst("secretKey")

    def test_initialization(self):
        """Test module has successfully initialized."""
        self.assertTrue(hasattr(self.waitlyst, "queue"))
        self.assertTrue(hasattr(self.waitlyst, "track"))
        self.assertTrue(hasattr(self.waitlyst, "identify"))
        self.assertTrue(hasattr(self.waitlyst, "set_anonymous_id"))
        self.assertTrue(hasattr(self.waitlyst, "page"))
        self.assertTrue(hasattr(self.waitlyst, "identity"))
        self.assertTrue(hasattr(self.waitlyst, "reset"))

    def test_set_anonymous_id(self):
        """Test setting anonymous id."""
        anonymous_id = str(uuid.uuid4())
        self.waitlyst.set_anonymous_id(anonymous_id)
        user = self.waitlyst.identity()

        # Assert the anonymous id has been set
        self.assertIsInstance(user, User)
        self.assertEqual(user.anonymous_id, anonymous_id)
        self.assertIsNone(user.id)

    @patch("waitlyst.http.HttpClient.post", side_effect=mockClient.handle_post)
    def test_identify(self, post):
        """Test that identifying events works."""
        self.waitlyst.identify(self.user_id)
        user = self.waitlyst.identity()

        # Assert that the user id has been set
        self.assertIsInstance(user, User)
        self.assertEqual(user.id, self.user_id)
        self.assertIsNone(user.anonymous_id)

    @patch("waitlyst.http.HttpClient.post", side_effect=mockClient.handle_post)
    def test_track(self, post):
        """Test that tracking events works."""
        self.waitlyst.reset()
        self.waitlyst.identify(self.user_id)
        self.waitlyst.track("test_track")

        # Assert that event has been successfully added.
        self.assertEqual(len(self.waitlyst.queue), 2)
        event = self.waitlyst.queue[1]
        self.assertIsInstance(event, TrackEvent)
        self.assertEqual(event.type, TrackEvent.type)

    @patch("waitlyst.http.HttpClient.post", side_effect=mockClient.handle_post)
    def test_page(self, post):
        """Test that page events works."""
        self.waitlyst.reset()
        self.waitlyst.identify(self.user_id)
        self.waitlyst.page("/page")

        # Assert that event has been successfully added.
        self.assertEqual(len(self.waitlyst.queue), 2)
        event = self.waitlyst.queue[1]
        self.assertIsInstance(event, PageEvent)
        self.assertEqual(event.type, PageEvent.type)

    @patch("waitlyst.http.HttpClient.post", side_effect=mockClient.handle_post)
    def test_user(self, post):
        """Test that the user object is returned."""
        self.waitlyst.reset()
        self.waitlyst.identify(self.user_id)
        user = self.waitlyst.identity()

        # Assert that the user object is returned.
        self.assertIsInstance(user, User)

    @patch("waitlyst.http.HttpClient.post", side_effect=mockClient.handle_post)
    def test_reset(self, post):
        """Test that user and queue information is purged."""
        self.waitlyst.identify(self.user_id)
        self.waitlyst.track("test_track")
        self.waitlyst.reset()

        # Assert that the user object is returned.
        self.assertEqual(len(self.waitlyst.queue), 0)
        self.assertIsNone(self.waitlyst.identity().id)
        self.assertIsNone(self.waitlyst.identity().anonymous_id)
