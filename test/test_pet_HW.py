import allure
import pytest
import requests
BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Store")
class TestOrder:
    @allure.title("Создание заказа")
    def test_create_order(self, create_order):
        with allure.step("Получение ID созданного заказа"):
            orderId = create_order["id"]

        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/{orderId}")

        with allure.step("Проверка статуса ответа"):
             assert response.status_code == 200

        with allure.step("Проверка параметров полей заказа в ответе"):
            response_json = response.json()
            assert response_json['id'] == create_order['id'], "id зказа не совпадает с ожидаемым"
            assert response_json['petId'] == create_order['petId'], "petId не совпадает с ожидаемым"
            assert response_json['quantity'] == create_order['quantity'], "quantity не совпадает с ожидаемым"
            assert response_json['status'] == create_order['status'], "status не совпадает с ожидаемым"
            assert response_json['complete'] == create_order['complete'], "complete не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_order(self):
        with allure.step("Отправка запроса на получение информации о заказе по ID"):
            response = requests.get(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа и данных заказа"):
            response_json = response.json()
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response_json['id'] == 1, "id зказа не совпадает с ожидаемым"
            assert response_json['petId'] == 1, "petId не совпадает с ожидаемым"
            assert response_json['quantity'] == 1, "quantity не совпадает с ожидаемым"
            assert response_json['status'] == "placed", "status не совпадает с ожидаемым"
            assert response_json['complete'] == True, "complete не совпадает с ожидаемым"

    @allure.title("Удаление заказа по ID")
    def test_delete_order(self):
        with allure.step("Отправка запроса на удаление заказа"):
            response = requests.delete(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа "):
            assert response.status_code == 200, "Заказ не удалось удалить"

        with allure.step("Отправка запроса на проверку удаленного заказа"):
            response = requests.get(f"{BASE_URL}/store/order/1")

        with allure.step("Проверка статуса ответа "):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка запроса на получение информации о несущесвующем заказе"):
            response = requests.get(f"{BASE_URL}/store/order/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка тестового содержимого ответа"):
            assert response.text == "Order not found", "Текст ответа не совпал с ожидаемым"


    @allure.title("Получение инвентаря в магазине")
    @pytest.mark.parametrize(
        "status, expected_value",
        [
            ("approved", 50),
            ("delivered", 50),
        ]
    )
    def test_get_store_inventory(self, status, expected_value):
        with allure.step("Отправка GET-запроса на /store/inventory"):
            response = requests.get(f"{BASE_URL}/store/inventory")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Статус код должен быть 200"

        with allure.step("Проверка формата данных"):
            inventory = response.json()
            assert isinstance(inventory, dict), "Ответ должен быть словарем"

        with allure.step("Проверка значений"):
            assert inventory.get(status) == expected_value, \
                f"Количество {status} заказов должно быть {expected_value}"