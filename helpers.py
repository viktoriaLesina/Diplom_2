import random
import string


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