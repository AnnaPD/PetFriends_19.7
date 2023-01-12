# PetFriends_19.7

1. Подумайте над вариантами тест-кейсов и напишите ещё 10 различных тестов для данного REST API-интерфейса (PetFriends).

Тест-кейсы:
1. TC-PF-1. Проверка невозможности авторизации с неверным паролем. Должен вывести статус код 403
2. TC-PF-2. Проверка возможности авторизации с корректными логином и паролем. Должен вывести статус код 200
3. TC-PF-3. Проверка запроса на возврат списка моих животных. Должен вывести статус код 200
4. TC-PF-4. Проверка невозможности добавить питомца с не корректными данными (спец.символы в наименовании параметров). Должен вывести статус код 400
5. TC-PF-5. Проверка невозможности обновления данных о питомце с некорректным ключом. Должен вывести статус код 403
         (Эта проверка не работает, статус кода при не верном auth_key не меняется, при этом питомцы удаляются. Такая же ситуация и на сайте с документацией Swagger.)
6. TC-PF-6. Проверка невозможности удаления питомца с некорректным ключом. Должен вывести статус код 403
7. TC-PF-7. Проверка возможности удаления питомца. Должен вывести статус код 200
8. TC-PF-8. Проверка невозможности удаления питомца с несуществующим pet_id. Должен вывести статус код 400
9. TC-PF-9. Проверка возможности добавления питомца без фото. Должен вывести статус код 200
10. TC-PF-10. Проверка возможности добавления фото питомца. Должен вывести статус код 200
         (В Swagger с этими же данными загружается в систему фото и статус 200. Здесь падает в ошибку.)
