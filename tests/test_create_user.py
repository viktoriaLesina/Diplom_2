import pytest
import requests

from data import ResponseMessages
from helpers import Helpers
from urls import Urls


class TestCreateUser:
    def test_create_unique_user(self, created_user):
        response = created_user['response']
        response_body = response.json()
        user_data = created_user['user_data']

        assert response.status_code == 200
        assert response_body['success'] is True
        assert response_body['user']['email'] == user_data['email']
        assert response_body['user']['name'] == user_data['name']
        assert 'accessToken' in response_body
        assert 'refreshToken' in response_body

    def test_create_existing_user_returns_error(self, created_user):
        user_data = created_user['user_data']

        response = requests.post(
            Urls.REGISTER_USER,
            json=user_data
        )

        response_body = response.json()

        assert response.status_code == 403
        assert response_body['success'] is False
        assert response_body['message'] == ResponseMessages.USER_ALREADY_EXISTS

    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_without_required_field_returns_error(
        self,
        missing_field
    ):
        user_data = Helpers.generate_user_data()
        user_data.pop(missing_field)

        response = requests.post(
            Urls.REGISTER_USER,
            json=user_data
        )

        response_body = response.json()

        assert response.status_code == 403
        assert response_body['success'] is False
        assert response_body['message'] == ResponseMessages.REQUIRED_FIELDS