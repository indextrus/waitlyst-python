from typing import Optional, List

from waitlyst.events import EventManager, Event
from waitlyst.exceptions import ErrorSecretKeyRequired
from waitlyst.http import HttpResponse
from waitlyst.models import User


class Waitlyst(object):
    secret_key: Optional[str] = None
    event_manager: Optional[EventManager] = None

    def __init__(self, secret_key: str, base_uri: str = None):
        self.secret_key = secret_key
        self.event_manager = EventManager(self.secret_key, base_uri=base_uri)
        self.initialize()

    def initialize(self):
        """Run through checks ensuring all necessary values are filled."""
        if not self.secret_key:
            raise ErrorSecretKeyRequired

    def identify(self, id: str = None, traits: Optional[dict] = None) -> HttpResponse:
        """Identify a user."""
        return self.event_manager.identify(id, traits)

    def set_anonymous_id(self, anonymous_id: str) -> User:
        """Set the anonymous id."""
        return self.event_manager.set_anonymous_id(anonymous_id)

    def track(self, event: str, properties: Optional[dict] = None) -> HttpResponse:
        """Track an event."""
        return self.event_manager.track(event, properties)

    def page(self, name: str, properties: Optional[dict] = None) -> HttpResponse:
        """Track a page view."""
        return self.event_manager.page(name, properties)

    def identity(self) -> User:
        """Get the current user."""
        return self.event_manager.identity()

    def group(self, id: str, traits: Optional[dict] = None) -> HttpResponse:
        """Track a group."""
        return self.event_manager.group(id, traits)

    def alias(self, new_id: str) -> HttpResponse:
        """Alias a user."""
        return self.event_manager.alias(new_id)

    def screen(self, name: str, properties: Optional[dict] = None) -> HttpResponse:
        """Track a screen view."""
        return self.event_manager.screen(name, properties)

    @property
    def queue(self) -> List[Event]:
        """Get the current queue."""
        return self.event_manager.queue

    def reset(self):
        """Resets the current context."""
        self.event_manager.reset()
        self.event_manager.queue = []
