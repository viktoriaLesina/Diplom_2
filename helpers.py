import random
import string

import allure
import requests

from urls import Urls


class Helpers:
    @staticmethod
    def generate_random_string(length=10):
        return ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=length)
        )

    @staticmethod
    def generate_user_data():
        random_part = Helpers.generate_random_string()

        return {
            'email': f'viktoriia_{random_part}@yandex.ru',
            'password': 'password123',
            'name': f'User_{random_part}'
        }


class ApiClient:
    @staticmethod
    @allure.step('Зарегистрировать пользователя')
    def register_user(user_data):
        return requests.post(Urls.REGISTER_USER, json=user_data)

    @staticmethod
    @allure.step('Авторизовать пользователя')
    def login_user(login_data):
        return requests.post(Urls.LOGIN_USER, json=login_data)

    @staticmethod
    @allure.step('Изменить данные пользователя')
    def update_user(user_data, access_token=None):
        headers = {'Authorization': access_token} if access_token else None
        return requests.patch(Urls.USER, headers=headers, json=user_data)

    @staticmethod
    @allure.step('Удалить пользователя')
    def delete_user(access_token):
        return requests.delete(
            Urls.USER,
            headers={'Authorization': access_token}
        )

    @staticmethod
    @allure.step('Получить список ингредиентов')
    def get_ingredients():
        return requests.get(Urls.INGREDIENTS)

    @staticmethod
    @allure.step('Создать заказ')
    def create_order(ingredient_ids, access_token=None):
        headers = {'Authorization': access_token} if access_token else None
        return requests.post(
            Urls.ORDERS,
            headers=headers,
            json={'ingredients': ingredient_ids}
        )

    @staticmethod
    @allure.step('Получить заказы пользователя')
    def get_user_orders(access_token=None):
        headers = {'Authorization': access_token} if access_token else None
        return requests.get(Urls.ORDERS, headers=headers)
