import uuid
from datetime import datetime
from typing import Optional, List

from requests import Response

from waitlyst.constants import API_PATHS, EVENT_TEMPLATE
from waitlyst.exceptions import (
    ErrorEventTypeRequired,
    ErrorEventNameRequired,
    ErrorInvalidPayload,
)
from waitlyst.http import HttpClient, HttpResponse
from waitlyst.models import User


class Event(object):
    type: str = None
    user_id: Optional[str] = None
    anonymous_id: Optional[str] = None
    timestamp: Optional[str] = None
    context: Optional[dict] = None
    message_id: Optional[str] = None
    received_at: Optional[str] = None
    sent_at: Optional[str] = None
    status: Optional[str] = None

    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        self.user_id = kwargs.get("userId")
        self.anonymous_id = kwargs.get("anonymousId")
        self.timestamp = kwargs.get("timestamp")
        self.context = kwargs.get("context")
        self.message_id = str(uuid.uuid4())
        self.received_at = datetime.now().isoformat()
        self.sent_at = datetime.now().isoformat()


class TrackEvent(Event):
    type = "track"
    event: str = None
    properties: Optional[dict] = None


class PageEvent(Event):
    type = "page"
    name: str = None
    properties: Optional[dict] = None


class IdentifyEvent(Event):
    type = "identify"
    traits: Optional[dict] = None


class EventManager(object):
    secret_key: str = None
    user: User = None
    client: HttpClient = None
    queue: List[Event] = []

    def __init__(self, secret_key: str, base_uri: str = None):
        self.secret_key = secret_key
        self.user = User()
        self.client = HttpClient(secret_key=secret_key, base_uri=base_uri)

    def set_anonymous_id(self, anonymous_id: str) -> User:
        self.user.anonymous_id = anonymous_id
        return self.user

    def reset(self):
        self.user = User()

    def identity(self) -> User:
        return self.user

    def construct(
        self, type: str, name: Optional[str] = None, props: Optional[dict] = None
    ) -> dict:
        """Constructs a payload in the appropriate format."""
        if not type:
            raise ErrorEventTypeRequired
        if not name and type != "identify":
            raise ErrorEventNameRequired
        now = datetime.now().isoformat("T", "milliseconds")
        payload = EVENT_TEMPLATE.copy()
        payload["anonymousId"] = self.user.anonymous_id
        payload["messageId"] = str(uuid.uuid4())
        payload["receivedAt"] = now
        payload["sentAt"] = now
        payload["timestamp"] = now
        payload["type"] = type
        payload["userId"] = self.user.id

        if type == "track":
            payload["event"] = name
            payload["properties"] = props
        elif type == "page":
            payload["name"] = props
            payload["properties"] = props
        elif type == "identify":
            payload["traits"] = props
            payload["userId"] = name

        return payload

    def create_event(self, payload):
        """Create an event object from a payload"""
        if payload["type"] == "track":
            return TrackEvent(**payload)
        elif payload["type"] == "page":
            return PageEvent(**payload)
        elif payload["type"] == "identify":
            return IdentifyEvent(**payload)
        else:
            raise ErrorInvalidPayload

    def handle(self, response: Response, payload: dict) -> HttpResponse:
        """Handle the response from the API."""
        event = self.create_event(payload)
        event.status = "success" if response.status_code == 200 else "error"
        http_response = HttpResponse(response)
        http_response.event = event

        # Push to queue
        self.queue.append(event)

        if response.status_code == 200 and payload["type"] == "identify":
            self.user.id = payload["userId"]

        return http_response

    def identify(self, id: str = None, traits: Optional[dict] = None) -> HttpResponse:
        payload = self.construct("identify", id, traits)
        response = self.client.post(path=API_PATHS["process_event"], data=payload)
        return self.handle(response, payload)

    def track(self, event: str, properties: Optional[dict] = None) -> HttpResponse:
        payload = self.construct("track", event, properties)
        response = self.client.post(path=API_PATHS["process_event"], data=payload)
        return self.handle(response, payload)

    def page(self, name: str, properties: Optional[dict] = None) -> HttpResponse:
        payload = self.construct("page", name, properties)
        response = self.client.post(path=API_PATHS["process_event"], data=payload)
        return self.handle(response, payload)
