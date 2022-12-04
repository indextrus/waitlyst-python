![Logo](./documentation/assets/waitlyst-github.png)

# waitlyst-python is a lightweight python library for tracking product analytics.

- Track every event on your app
- Understand your users and how to improve your product

## Documentation
Please visit https://waitlyst.co/docs to view the complete documentation.

## Getting Started
This module is distributed via pypi. You can install it using pip:


```sh
pip install waitlyst-python
```

## Tracking product analytics
![Logo](./documentation/assets/github-analytics.png)

#### Using waitlyst-python:

```python
from waitlyst.index import Waitlyst

waitlyst = Waitlyst('YOUR_SECRET_KEY')

# Before tracking any event, you need to identify the user
waitlyst.identify('USER_ID')

waitlyst.identify('USER_ID', {
    'firstName': 'John',
    'lastName': 'Doe',
    'email': 'test@example.com'
})

# or you can use an anonymous id if you don't have a user id
# when you identify a user with an anonymous id, waitlyst will automatically
# reconcile the user in your dashboard
waitlyst.set_anonymous_id('ANONYMOUS_ID')


# Tracking pageviews
waitlyst.page('Home Page')

waitlyst.page('/homepage')

waitlyst.page('/homepage', {
    'url': 'https://example.com/homepage/',
    'title': 'Home page'
})

# Track a custom event
waitlyst.track('itemPurchased', {
    "price": 3000,
    "id": '1234',
    "quantity": 1 
})
```