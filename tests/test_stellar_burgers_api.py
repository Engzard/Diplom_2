import requests
import allure
from date import URL


class TestStellarBurgersAPI:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, unique_user_data):
        response = requests.post(f"{URL}/auth/register", json=unique_user_data)
        assert (response.status_code == 200) and (response.json()["success"] == True)

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_duplicate_user_failure(self, existing_user_data):
        response = requests.post(f"{URL}/auth/register", json=existing_user_data)
        assert (response.status_code == 403) and (response.json()["success"] == False)

    @allure.title("Создание пользователя без email")
    def test_create_user_missing_email_field(self, unique_user_data):
        user_data = unique_user_data
        del user_data["email"]
        response = requests.post(f"{URL}/auth/register", json=user_data)
        assert (response.status_code == 403) and (response.json()["success"] == False)

    @allure.title("Создание пользователя без password")
    def test_create_user_missing_password_field(self, unique_user_data):
        user_data = unique_user_data
        del user_data["password"]
        response = requests.post(f"{URL}/auth/register", json=user_data)
        assert (response.status_code == 403) and (response.json()["success"] == False)

    @allure.title("Создание пользователя без name")
    def test_create_user_missing_name_field(self, unique_user_data):
        user_data = unique_user_data
        del user_data["name"]
        response = requests.post(f"{URL}/auth/register", json=user_data)
        assert (response.status_code == 403) and (response.json()["success"] == False)

    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user_success(self, existing_user_data):
        login_data = {
            "email": existing_user_data["email"],
            "password": existing_user_data["password"]
        }
        response = requests.post(f"{URL}/auth/login", json=login_data)
        assert (response.status_code == 200) and (response.json()["success"] == True)

    @allure.title("Вход с неверным паролем")
    def test_login_with_wrong_password_failure(self, existing_user_data):
        login_data = {
            "email": existing_user_data["email"],
            "password": "wrong_password"
        }
        response = requests.post(f"{URL}/auth/login", json=login_data)
        assert (response.status_code == 401) and (response.json()["success"] == False)

    @allure.title("Вход с неверным email")
    def test_login_with_wrong_email_failure(self, existing_user_data):
        login_data = {
            "email": "wrong_@email.ru",
            "password": existing_user_data["password"]
        }
        response = requests.post(f"{URL}/auth/login", json=login_data)
        assert (response.status_code == 401) and (response.json()["success"] == False)

    @allure.title("Вход без email")
    def test_login_missing_email_field(self, existing_user_data):
        login_data = {
            "password": existing_user_data["password"]
        }
        response = requests.post(f"{URL}/auth/login", json=login_data)
        assert (response.status_code == 403) and (response.json()["success"] == False)

    @allure.title("Вход без password")
    def test_login_missing_password_field(self, existing_user_data):
        login_data = {
            "email": existing_user_data["email"]
        }
        response = requests.post(f"{URL}/auth/login", json=login_data)
        assert (response.status_code == 403) and (response.json()["success"] == False)

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_success(self, existing_user_data):
        login_data = {
            "email": existing_user_data["email"],
            "password": existing_user_data["password"]
        }
        login_response = requests.post(f"{URL}/auth/login", json=login_data)
        assert login_response.status_code == 200
        order_data = {
            "ingredients": ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]
        }
        response = requests.post(f"{URL}/orders", json=order_data)
        assert response.status_code == 200 and response.json()["success"] == True

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_failure(self):
        order_data = {
            "ingredients": ["60d3b41abdacab0026a733c6", "609646e4dc916e00276b2870"]
        }
        response = requests.post(f"{URL}/orders", json=order_data)
        assert response.status_code == 401 and response.json()["success"] == False

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_failure(self, existing_user_data):
        login_data = {
            "email": existing_user_data["email"],
            "password": existing_user_data["password"]
        }
        login_response = requests.post(f"{URL}/auth/login", json=login_data)
        assert login_response.status_code == 200
        order_data = {
            "ingredients": []
        }
        response = requests.post(f"{URL}/orders", json=order_data)
        assert response.status_code == 400 and response.json()["success"] == False

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_failure(self, existing_user_data):
        login_data = {
            "email": existing_user_data["email"],
            "password": existing_user_data["password"]
        }
        login_response = requests.post(f"{URL}/auth/login", json=login_data)
        assert login_response.status_code == 200
        order_data = {
            "ingredients": ["wrong", "wrong"]
        }
        response = requests.post(f"{URL}/orders", json=order_data)
        assert response.status_code == 400 and response.json()["success"] == False