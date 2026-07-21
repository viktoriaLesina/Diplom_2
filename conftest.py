import pytest

from helpers import ApiClient, Helpers


@pytest.fixture
def users_to_delete():
    access_tokens = []

    yield access_tokens

    for access_token in access_tokens:
        ApiClient.delete_user(access_token)


@pytest.fixture
def created_user():
    user_data = Helpers.generate_user_data()
    response = ApiClient.register_user(user_data)
    response_body = response.json()

    user = {
        'user_data': user_data,
        'access_token': response_body.get('accessToken')
    }

    yield user

    if user['access_token']:
        ApiClient.delete_user(user['access_token'])
