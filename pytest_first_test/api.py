
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """Api библиотека к веб-приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключом пользователя, найденного по указанным email и паролем"""

        headers = {
            'email': email,
            'password': password,
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "my_pets") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь
        либо пустое значение - получить список всех питомцев, либо 'my_pets' - получить список
        собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image\jpg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

    def add_photo_to_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер фото к добавленному ранее питомцу. Возвращает статус
        запроса и данные питомца в JSON."""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet_without_photo(self, auth_key: json, name: str,
                                  animal_type: str, age: int) -> json:

        """Метод отправляет на сервер информацию о новом питомце без фото, и возвращает статус
        запроса и данные о нём в JSON."""

        headers = {'auth_key': auth_key['key']}

        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def create_new_pet(self, auth_key: json, name: str, animal_type: str, age: str):
        """Метод предназначен для создания нового питомца на сайте PetFriends с помощью запроса POST,
        переданного в формате JSON"""

        data = {'name': name,
                'animal_type': animal_type,
                'age': age,
                }
        header = {'auth_key': auth_key['key']}
        resp = requests.post(self.base_url + '/api/create_pet_simple', headers=header, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        print(result)
        return status, result

    def get_list_pets(self, auth_key: json, filter: str = ''):
        """Метод делает запрос и получает ответ в формате json со списком всех питомцев
        зарегистрированных на сайте PetFriends. С помощью фильтра my_pets можно получить список питомцев,
        внесенных пользователем"""

        header = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        resp = requests.get(self.base_url + '/api/pets', headers=header, params=filter)
        status = resp.status_code
        result = resp.json()
        return status, result

    def set_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str):
        """Метод предназначен для создания нового питомца на сайте PetFriends с помощью запроса POST,
        переданного в формате JSON"""

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                    })
        header = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        resp = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=header, data=data)
        status = resp.status_code
        result = ''
        try:
            result = resp.json()
        except json.decoder.JSONDecodeError:
            result = resp.text
        print(result)
        return status, result