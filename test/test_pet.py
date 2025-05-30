from http.client import responses

import allure
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего животного")
    def test_deleted_nonexistent_pet(self):
        with allure.step("Отправка запроса на несуществующего животного"):
            response = requests.delete(url = f"{BASE_URL}/pet/9999")
            print(response)
        with allure.step("Проверка статуса ответа"):
            assert  response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка тестового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ответа не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего животного")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несущесвующего питомца"):
            payload = {"id": 9999,
                       "name": "Non-existent Pet",
                       "status": "available"
                       }
            response = requests.put(f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert  response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка тестового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ответа не совпал с ожидаемым"


    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несущесвующем питомце"):

            response = requests.get(f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка тестового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ответа не совпал с ожидаемым"