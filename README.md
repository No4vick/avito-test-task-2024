# Тестовое задание для стажёра Backend Авито

## Стек

### Сервер

* Python 3.12.2
* FastAPI

### База данных
* PostgreSQL

### Тесты
* unittests

## Запуск
Склонируйте проект
```
git clone https://github.com/No4vick/avito-test-task-2024.git
```
Соберите образы docker:
```
docker-compose up --build
```
Сервер будет запущен на порте 8000
Также можно указать количество потоков в Dockerfile
```
WORKER_COUNT = 4 # Или другое целое значение больше 0
```
Можно просмотреть Swagger по эндпоинту `/docs`

## Тестирование
Установите зависимости:
```
pip install requirements-test.txt
```

## Заметки
* Так как не сказано, как заданы токены пользователей и админов, использовалась таблица из базы данных
* Так как параметры tag_ids и feature_id необязательны, то при неуказании возвращается всё
* У меня было мало времени, поэтому что-то может работать неправильно или не работать вообще
* Так как в FastAPI автогенерируемая OpenAPI документация, то она немного не сходится с данной
