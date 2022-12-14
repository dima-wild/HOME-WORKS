# from api import PetFriends
# from settings import valid_email, valid_password
#
# pf = PetFriends()
#
#
# def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
#     status, result = pf.get_api_key(email, password)
#     assert status == 200
#     assert 'key' in result
#
# def test_get_all_pets_with_valid_key(filter=''):
#     _, auth_key = pf.get_api_key(valid_email, valid_password)
#     status, result = pf.get_list_of_pets(auth_key, filter)
#     assert status == 200
#     assert len(result['pets']) > 0

import pytest
from api import PetFriends
from settings import *
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями.
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """ Проверяем что запрос api-ключа возвращает статус 403 при входе неавторизованного юзера."""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result.
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями.
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев, и проверяем что он не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_get_all_my_pets_with_valid_key(filter='my_pets'):
    """ Проверка своего списка, который может быть и пустым."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) >= 0


def test_add_new_pet_with_valid_data(name='Кори', animal_type='Собака',
                                     age='4', pet_photo='images\corey.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo.
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем — если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев.
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "", "", '', "images\jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление.
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца.
    assert status == 200
    assert pet_id not in my_pets.values()


def test_add_new_pet_without_photo(name='Марта', animal_type='собака', age=0):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменную auth_key.
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом.
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Марта', animal_type='собака', age=1):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст.
    if len(my_pets['pets']) > 1:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][1]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному.
        assert status == 200
        assert result['name'] == name
    else:
        # Если список пустой, то выкидываем исключение с текстом об отсутствии своих питомцев.
        raise Exception("There is no my pets")

def test_create_new_pet(name='', animal_type='', age=''):
    """Негативная проверка простого создания нового питомца c пустыми полями. Результат - успешный -> присутствует
    баг сервера (баг-репорт)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet(auth_key, name, animal_type, age)
    _, my_pets = pf.get_list_pets(auth_key, 'my_pets')
    assert status == 200
    assert result['name'] == name


def test_set_photo_pet(pet_photo='images/corey.jpg'):
    """Проверка добавления фотографии к данным существующего питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_pets(auth_key, 'my_pets')
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.set_photo_pet(auth_key, pet_id, pet_photo)
    _, my_pets = pf.get_list_pets(auth_key)
    assert status == 200
    assert result['pet_photo'] is not None
