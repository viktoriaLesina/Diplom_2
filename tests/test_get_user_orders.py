import allure

from data import ResponseMessages
from helpers import ApiClient


@allure.feature('Получение заказов пользователя')
class TestGetUserOrders:
    @staticmethod
    @allure.step('Получить идентификаторы двух ингредиентов')
    def get_two_ingredient_ids():
        ingredients = ApiClient.get_ingredients().json()['data']
        return [ingredients[0]['_id'], ingredients[1]['_id']]

    @allure.title('Получение заказов авторизованного пользователя')
    def test_get_orders_authorized_user(self, created_user):
        ApiClient.create_order(
            self.get_two_ingredient_ids(),
            created_user['access_token']
        )

        response = ApiClient.get_user_orders(created_user['access_token'])
        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert 'orders' in response_body
        assert len(response_body['orders']) > 0
        assert 'total' in response_body
        assert 'totalToday' in response_body

    @allure.title('Получение заказов без авторизации')
    def test_get_orders_unauthorized_user_returns_error(self):
        response = ApiClient.get_user_orders()
        response_body = response.json()

        assert response.status_code == 401
        assert response_body['success'] is False
        assert response_body['message'] == ResponseMessages.SHOULD_BE_AUTHORISED
