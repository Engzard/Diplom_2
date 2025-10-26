import requests
import pytest
from date import URL
from helpers import generate_random_string


@pytest.fixture
def unique_user_data():
    email = f"{generate_random_string(10)}@yandex.ru"
    name = f'{generate_random_string(10)}'
    return {
        "email": email,
        "password": "999123",
        "name": name
    }


@pytest.fixture
def existing_user_data():
    email = f"{generate_random_string(10)}@yandex.ru"
    name = f'{generate_random_string(10)}'
    user_data = {
        "email": email,
        "password": "999123",
        "name": name
    }
    response = requests.post(f"{URL}/auth/register", json=user_data)

    yield user_data
    response = requests.delete(f"{URL}/auth/user ", json=user_data)
