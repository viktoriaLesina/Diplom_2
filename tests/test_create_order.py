import allure

from data import ResponseMessages
from helpers import ApiClient


@allure.feature('Создание заказа')
class TestCreateOrder:
    @staticmethod
    @allure.step('Получить идентификаторы двух ингредиентов')
    def get_two_ingredient_ids():
        ingredients = ApiClient.get_ingredients().json()['data']
        return [ingredients[0]['_id'], ingredients[1]['_id']]

    @allure.title('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_authorization_and_ingredients(
        self,
        created_user
    ):
        response = ApiClient.create_order(
            self.get_two_ingredient_ids(),
            created_user['access_token']
        )
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert 'order' in response_body
        assert 'number' in response_body['order']

    @allure.title('Создание заказа без авторизации с ингредиентами')
    def test_create_order_without_authorization_with_ingredients(self):
        response = ApiClient.create_order(self.get_two_ingredient_ids())
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert 'order' in response_body
        assert 'number' in response_body['order']

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients_returns_error(
        self,
        created_user
    ):
        response = ApiClient.create_order(
            [],
            created_user['access_token']
        )
        response_body = response.json()

        assert response.status_code == 400
        assert response_body['success'] is False
        assert response_body['message'] == ResponseMessages.INGREDIENT_IDS_REQUIRED

    @allure.title('Создание заказа с неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredient_hash_returns_error(
        self,
        created_user
    ):
        response = ApiClient.create_order(
            ['invalid_ingredient_hash'],
            created_user['access_token']
        )

        assert response.status_code == 500
