# sovabet
Система учёта турнира прогнозистов "Совабет" квиза "Кубок Совы".

## Используемые технологии
Язык программирования:
- Python 3.10

Сторонние библиотеки:
- Django
- django-environ
- django-import-export
- gunicorn
- psycopg2-binary
- vk

## Предварительные действия
Создайте и активируйте виртуальное окружение в главной директории проекта `sovabet`:
```
$ python3.10 -m venv .venv
$ source .venv/bin/activate
(.venv) $
```
Установите зависимости из `requirements.txt`:
```
(.venv) $ pip install -r requirements.txt
```
Перейдите в дочернюю директорию `src`:
```
(.venv) $ cd src/
```
Создайте файл `.env` (либо переименуйте `.env_sample`). Заполните значения переменных окружения:
```
DEBUG=
SECRET_KEY=
DATABASE_URL=
VK_ACCESS_TOKEN=
VK_API_VERSION=
VK_OWNER_ID=
ALLOWED_HOSTS=
```

## Запуск
Примените миграции базы данных:
```
(.venv) $ python3 manage.py migrate
```
Создайте суперпользователя:
```
(.venv) $ python3 manage.py createsuperuser
```
Локальный веб-сервер запускается следующей командой:
```
(.venv) $ python3 manage.py runserver
```

## Автор
Александр Аравин - [sander-raven](https://github.com/sander-raven). Email: sander-raven@yandex.ru.

## Лицензия
Проект находится под лицензией MIT. Подробнее: смотри файл [LICENSE](LICENSE).
