from http.client import responses

import allure
import jsonschema
import requests
from .schemas.pet_schemas import PET_SCHEMA
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

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для добавления нового питомца"):
            payload = {
                        "id": 1,
                        "name": "Buddy",
                        "status": "available"
                      }

        with allure.step("Отправка запроса на создания питомца"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Текст ответа не совпал с ожидаемым"
            jsonschema.validate(response_json,PET_SCHEMA)


        with allure.step("Проверка параметров полей питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"


    @allure.title("Добавление нового питомца с полными данными")
    def test_add_full_pet(self):
        with allure.step("Подготовка данных для добавления нового питомца с полними данными"):
            payload = {"id": 10,
                       "name": "doggie",
                       "category": {
                           "id": 1,
                           "name": "Dogs"
                       },
                       "photoUrls": ["string"],
                       "tags": [{"id": 0,
                                 "name": "string"
                                 }],
                       "status": "available"}

        with allure.step("Отправка запроса на создания питомца с полными данными"):
            response = requests.post(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200, "Текст ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров полей питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "категория питомца не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "фото-url питомца не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "тэги питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "статус питомца не совпадает с ожидаемым"
