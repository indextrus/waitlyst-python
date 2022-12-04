from typing import Optional


class User(object):
    id: Optional[str] = None
    anonymous_id: Optional[str] = None

    def __init__(self, id: str = None, anonymous_id: str = None):
        self.id = id
        self.anonymous_id = anonymous_id

    def __str__(self):
        return f"User(id={self.id}, anonymous_id={self.anonymous_id})"

    def __repr__(self):
        return self.__str__()

    def reset(self):
        """Reset the user to an anonymous user."""
        self.id = None
        self.anonymous_id = None
