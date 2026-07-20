import allure

from data import ResponseMessages
from helpers import ApiClient


@allure.feature('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Авторизация существующего пользователя')
    def test_login_existing_user(self, created_user):
        user_data = created_user['user_data']
        login_data = {
            'email': user_data['email'],
            'password': user_data['password']
        }

        response = ApiClient.login_user(login_data)
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert response_body['user']['email'] == user_data['email']
        assert response_body['user']['name'] == user_data['name']
        assert 'accessToken' in response_body
        assert 'refreshToken' in response_body

    @allure.title('Авторизация с неверными учётными данными')
    def test_login_with_incorrect_credentials_returns_error(self, created_user):
        user_data = created_user['user_data']
        login_data = {
            'email': user_data['email'],
            'password': 'incorrect_password'
        }

        response = ApiClient.login_user(login_data)
        response_body = response.json()

        assert response.status_code == 401
        assert response_body['success'] is False
        assert response_body['message'] == ResponseMessages.INCORRECT_LOGIN_DATA
