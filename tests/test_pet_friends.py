from api import PetFriends
from settings import valid_email, valid_password, not_valid_password
import os

pf = PetFriends()

# TC-PF-1
def test_get_api_key_for_not_valid_user(email=valid_email, password=not_valid_password):
    """ Проверяем что запрос api ключа возвращает статус 403 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    print('Не верно указан логин или пароль')

# TC-PF-2
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result
    print('Ключ:', result)

# TC-PF-3
def test_get_all_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос моих питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем, что список моих питомцев не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0
    print('Мои питомцы:\n', result)

# TC-PF-4
def test_add_new_pet_with_valid_data(name='(/\*+)', animal_type='__--__',
                                     age='?', pet_photo='images/Dog.jpg'):
    """Проверяем, что невозможно добавить питомца с не корректными данными (в виде символов)"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Запрашиваем список своих питомцев my_pets и выводим pet_id добавленного питомца
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    print('ID добавленного питомца:', pet_id)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400 # Проходит загрузка не корректных данных со статусом 200. Ошибка не отлавливается (возможно нет ограничения по вводу для полей на бэке и фронте). И ещё невозможно проверить ошибку, если поля не заполнены (система не читает код).
    assert result['name'] == name

# TC-PF-5
def test_successful_update_self_pet_info_auth_key(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце с некорректным auth_key"""

    auth_key = '10000001'
    print(auth_key)
    pet_id = 'pet_id'
    status, result = pf.update_pet_info_auth_key(auth_key, pet_id, name, animal_type, age)

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 403
    print('Предоставленные данные не верны. Проверьте правильность написания auth_key')

# TC-PF-6
def test_successful_delete_self_pet_auth_key():
    """Проверяем возможность удаления питомца при не верном auth_key"""

    auth_key = '10000001'
    print(auth_key)
    pet_id = 'pet_id'

    # Берём id первого питомца из списка и отправляем запрос на удаление

    status, _ = pf.delete_pet_auth_key(auth_key, pet_id)

     # Проверяем что статус ответа равен 403
    assert status == 403 # Эта проверка не работает, статус кода при не верном auth_key не меняется, при этом питомцы удаляются. Такая же ситуация и на сайте с документацией.
    print('Предоставленные данные не верны. Проверьте правильность написания auth_key')

# TC-PF-7
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Макака", "обезьянка", "3", "images/Lion.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    print('ID удаляемого питомца:', pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

# TC-PF-8
def test_successful_update_self_pet_info_pet_id(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце с несуществующим pet_id"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Пробуем обновить  имя, тип и возраст при несуществующем id питомца
    pet_id = 'pet_id'
    status, result = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

        # Проверяем что статус ответа = 400 и такого питомца не существует
    assert status == 400
    print('Предоставленные данные не верны. Проверьте правильность написания pet_id')

# TC-PF-9
def test_add_new_pet_not_photo(name='Дракула', animal_type='летучая мышь',
                                     age='1'):
    """Проверяем что можно добавить питомца без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# TC-PF-10
def test_add_pet_photo(pet_photo='images/Dog.jpg'):
    """Проверяем, что можно добавить фото питомца"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    print('auth_key:', auth_key)

    # Запрашиваем список своих питомцев my_pets и выводим pet_id питомца
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    print('ID добавленного питомца:', pet_id)

    # Добавляем фото питомца
    status, _ = pf.post_api_pets_set_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200 # В Swagger с этими же данными загружается в систему фото и статус 200. Здесь падает в ошибку.

