class BaseException(Exception):
    """Base class for all exceptions."""

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return self.message


class ErrorSecretKeyRequired(BaseException):
    message = "You must set a secret key to use waitlyst."


class ErrorEventTypeRequired(Exception):
    message = "You must set an event type."


class ErrorEventNameRequired(Exception):
    message = "You must set an name for this event."


class ErrorInvalidPayload(Exception):
    message = "The payload is invalid."
