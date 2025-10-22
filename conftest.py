import requests
import pytest
from date import URL
from helpers import generate_random_string


@pytest.fixture
def unique_user_data():
    """Генерирует данные для уникального пользователя"""
    email = f"{generate_random_string(10)}@yandex.ru"
    name = f'{generate_random_string(10)}'
    return {
        "email": email,
        "password": "999123",
        "name": name
    }


@pytest.fixture
def existing_user_data():
    """Создает и возвращает данные существующего пользователя"""
    email = f"{generate_random_string(10)}@yandex.ru"
    name = f'{generate_random_string(10)}'
    user_data = {
        "email": email,
        "password": "999123",
        "name": name
    }
    response = requests.post(f"{URL}/auth/register", json=user_data)
    assert response.status_code == 200

    return user_data
