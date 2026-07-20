import allure
import pytest

from data import ResponseMessages
from helpers import ApiClient, Helpers


@allure.feature('Создание пользователя')
class TestCreateUser:
    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self):
        user_data = Helpers.generate_user_data()
        response = ApiClient.register_user(user_data)
        response_body = response.json()

        try:
            assert response.status_code == 200
            assert response_body['success'] is True
            assert response_body['user']['email'] == user_data['email']
            assert response_body['user']['name'] == user_data['name']
            assert 'accessToken' in response_body
            assert 'refreshToken' in response_body
        finally:
            access_token = response_body.get('accessToken')
            if access_token:
                ApiClient.delete_user(access_token)

    @allure.title('Создание уже зарегистрированного пользователя')
    def test_create_existing_user_returns_error(self, created_user):
        response = ApiClient.register_user(created_user['user_data'])
        response_body = response.json()

        assert response.status_code == 403
        assert response_body['success'] is False
        assert response_body['message'] == ResponseMessages.USER_ALREADY_EXISTS

    @allure.title('Создание пользователя без обязательного поля: {missing_field}')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_without_required_field_returns_error(
        self,
        missing_field
    ):
        user_data = Helpers.generate_user_data()
        user_data.pop(missing_field)

        response = ApiClient.register_user(user_data)
        response_body = response.json()

        assert response.status_code == 403
        assert response_body['success'] is False
        assert response_body['message'] == ResponseMessages.REQUIRED_FIELDS
