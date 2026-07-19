import pytest
import requests

from data import ResponseMessages
from urls import Urls


class TestUpdateUser:
    @pytest.mark.parametrize(
        'field,new_value',
        [
            ('email', 'updated_user@yandex.ru'),
            ('password', 'new_password_123'),
            ('name', 'Updated User')
        ]
    )
    def test_update_user_with_authorization(
        self,
        created_user,
        field,
        new_value
    ):
        access_token = created_user['access_token']

        response = requests.patch(
            Urls.USER,
            headers={'Authorization': access_token},
            json={field: new_value}
        )

        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True

        if field == 'email':
            assert response_body['user']['email'] == new_value
        elif field == 'name':
            assert response_body['user']['name'] == new_value

    @pytest.mark.parametrize(
        'field,new_value',
        [
            ('email', 'unauthorized_user@yandex.ru'),
            ('password', 'unauthorized_password'),
            ('name', 'Unauthorized User')
        ]
    )
    def test_update_user_without_authorization_returns_error(
        self,
        field,
        new_value
    ):
        response = requests.patch(
            Urls.USER,
            json={field: new_value}
        )

        response_body = response.json()

        assert response.status_code == 401
        assert response_body['success'] is False
        assert response_body['message'] == ResponseMessages.SHOULD_BE_AUTHORISED