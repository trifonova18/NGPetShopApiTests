from http.client import responses

import allure
import jsonschema
import pytest
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

    @allure.title("Получение информации питомца по ID")
    def test_get_pet_by_id(self,create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id=create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert  response.status_code == 200
            assert  response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_updated_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
             assert response.status_code == 200

        with allure.step("Подготовка данных для обновления созданного питомца"):
            payload = {"id": pet_id,
                       "name": "Buddy Updated",
                       "status": "sold"
                       }

        with allure.step("Отправка запроса на обновление созданного питомца"):
            response = requests.put(f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка обновленных параметров полей питомца в ответе"):
            assert response.status_code == 200
            assert response_json['name'] == payload['name'], "имя питомца не совпадает с ожидаемым"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Отправка запроса на удаление питомца по ID"):
            response = requests.delete(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Не удалось удалить питомца"

        with allure.step("Попытка отправить запрос на получение информации об удаленном питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [
            ("available", 200),
            ("sold", 200),
            ("notavailable", 400),
            ("", 400),
        ]
    )
    def test_get_pet_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status":status})

        with allure.step("Проверка статуса ответа и формата данных"):
            assert (expected_status_code == 200 and isinstance(response.json(), list)) or (
                    expected_status_code == 400 and not isinstance(response.json(), list)
                ) "проверка"


