import requests

from data import ResponseMessages
from urls import Urls


class TestGetUserOrders:
    def test_get_orders_authorized_user(self, created_user):
        ingredients_response = requests.get(Urls.INGREDIENTS)
        ingredients = ingredients_response.json()['data']

        ingredient_ids = [
            ingredients[0]['_id'],
            ingredients[1]['_id']
        ]

        create_order_response = requests.post(
            Urls.ORDERS,
            headers={
                'Authorization': created_user['access_token']
            },
            json={
                'ingredients': ingredient_ids
            }
        )

        assert create_order_response.status_code == 200

        response = requests.get(
            Urls.ORDERS,
            headers={
                'Authorization': created_user['access_token']
            }
        )

        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert 'orders' in response_body
        assert len(response_body['orders']) > 0
        assert 'total' in response_body
        assert 'totalToday' in response_body

    def test_get_orders_unauthorized_user_returns_error(self):
        response = requests.get(Urls.ORDERS)

        response_body = response.json()

        assert response.status_code == 401
        assert response_body['success'] is False
        assert response_body['message'] == ResponseMessages.SHOULD_BE_AUTHORISED