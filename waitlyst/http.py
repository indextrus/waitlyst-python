from typing import Any

import requests
from requests import Response


class HttpResponse(object):
    response: Response = None
    event: Any = None

    def __init__(self, response: Response):
        self.response = response


class HttpClient(object):
    base_url: str = None
    headers: dict = {}

    def __init__(self, base_url: str = None):
        self.base_url = base_url or "https://api.waitlyst.com/v1"

    def set_headers(self, headers: dict):
        """Set the headers for the HTTP client."""
        self.headers = headers

    def post(self, path: str, data: dict, headers: dict = None) -> Response:
        """Send a POST request to the API."""
        if headers is None:
            headers = self.headers
        url = f"{self.base_url}{path}"
        response = requests.post(url=url, json=data, headers=headers)
        return response

    def get(self, path: str, params: dict, headers: dict = None) -> Response:
        """Send a GET request to the API."""
        if headers is None:
            headers = self.headers
        url = f"{self.base_url}{path}"
        response = requests.get(url, params=params, headers=headers)
        return response

    def put(self, path: str, data: dict, headers: dict = None) -> Response:
        """Send a PUT request to the API."""
        if headers is None:
            headers = self.headers
        url = f"{self.base_url}{path}"
        response = requests.put(url, json=data, headers=headers)
        return response

    def patch(self, path: str, data: dict, headers: dict = None) -> Response:
        """Send a PATCH request to the API."""
        if headers is None:
            headers = self.headers
        url = f"{self.base_url}{path}"
        response = requests.patch(url, json=data, headers=headers)
        return response

    def delete(self, path: str, headers: dict = None) -> Response:
        """Send a DELETE request to the API."""
        if headers is None:
            headers = self.headers
        url = f"{self.base_url}{path}"
        response = requests.delete(url, headers=headers)
        return response
