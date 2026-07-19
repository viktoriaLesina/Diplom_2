import requests

from data import ResponseMessages
from urls import Urls


class TestCreateOrder:
    def test_create_order_with_authorization_and_ingredients(
        self,
        created_user
    ):
        ingredients_response = requests.get(Urls.INGREDIENTS)
        ingredients = ingredients_response.json()['data']

        ingredient_ids = [
            ingredients[0]['_id'],
            ingredients[1]['_id']
        ]

        response = requests.post(
            Urls.ORDERS,
            headers={
                'Authorization': created_user['access_token']
            },
            json={
                'ingredients': ingredient_ids
            }
        )

        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert 'order' in response_body
        assert 'number' in response_body['order']

    def test_create_order_without_authorization_with_ingredients(self):
        ingredients_response = requests.get(Urls.INGREDIENTS)
        ingredients = ingredients_response.json()['data']

        ingredient_ids = [
            ingredients[0]['_id'],
            ingredients[1]['_id']
        ]

        response = requests.post(
            Urls.ORDERS,
            json={
                'ingredients': ingredient_ids
            }
        )

        response_body = response.json()

        assert response.status_code == 200
        assert response_body['success'] is True
        assert 'order' in response_body
        assert 'number' in response_body['order']

    def test_create_order_without_ingredients_returns_error(
        self,
        created_user
    ):
        response = requests.post(
            Urls.ORDERS,
            headers={
                'Authorization': created_user['access_token']
            },
            json={
                'ingredients': []
            }
        )

        response_body = response.json()

        assert response.status_code == 400
        assert response_body['success'] is False
        assert (
            response_body['message']
            == ResponseMessages.INGREDIENT_IDS_REQUIRED
        )

    def test_create_order_with_invalid_ingredient_hash_returns_error(
        self,
        created_user
    ):
        response = requests.post(
            Urls.ORDERS,
            headers={
                'Authorization': created_user['access_token']
            },
            json={
                'ingredients': ['invalid_ingredient_hash']
            }
        )

        assert response.status_code == 500