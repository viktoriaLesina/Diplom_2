import pytest
import requests

from helpers import Helpers
from urls import Urls


@pytest.fixture
def created_user():
    user_data = Helpers.generate_user_data()

    response = requests.post(
        Urls.REGISTER_USER,
        json=user_data
    )

    assert response.status_code == 200, (
        f'Не удалось создать тестового пользователя: {response.text}'
    )

    response_body = response.json()
    access_token = response_body['accessToken']

    yield {
        'user_data': user_data,
        'access_token': access_token,
        'response': response
    }

    requests.delete(
        Urls.USER,
        headers={'Authorization': access_token}
    )