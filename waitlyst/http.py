from typing import Any

import requests
from requests import Response


class HttpResponse(object):
    response: Response = None
    data: dict = None
    status_code: int = None
    status: str = None
    event: Any = None

    def __init__(self, response: Response):
        self.response = response
        self.data = response.json()
        self.status_code = response.status_code
        self.status = "success" if response.status_code == 200 else "failed"


class HttpClient(object):
    base_url: str = None
    secret_key: str = None
    headers: dict = {}

    def __init__(self, secret_key: str, base_uri: str = None):
        self.secret_key = secret_key
        self.base_url = base_uri or "https://api.waitlyst.co/v1"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.secret_key}",
        }
        self.set_headers(headers)

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
