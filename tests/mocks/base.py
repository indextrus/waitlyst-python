import json

from waitlyst.constants import API_PATHS


class MockResponse:
    def __init__(self, text_data=None, json_data=None, status_code=None):
        self.json_data = json_data
        self.text = text_data
        self.status_code = status_code

    def json(self):
        return json.loads(self.text)


class MockHttpClient(object):
    def handle_post(*args, **kwargs):
        if kwargs["path"] in f"{API_PATHS['process_event']}":
            data = """{
                "expires_in": "fred.example@gmail.com"
            }"""
            return MockResponse(text_data=data, status_code=200)
