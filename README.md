# Описание

1. Проект из себя представляет API для проекта "api_final_yatube"

2. Он решает такие задачи как:
1) Обработка GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS запросов
2) Работа с JWT токенами
3) Сериализация, десериализация и валидация данных

3.Польза его заключается в том, что он помогает пользователю взаимодействовать с сервером


# Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/kittygram.git
```

```
cd kittygram
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

# Примеры запросов к API

1) Для создания токена нужно выполнить такой запрос "http://127.0.0.1:8000/api/v1/jwt/create/", где указываем поля "username" и "password" 

2) Для создания поста выполняем запрос "http://127.0.0.1:8000/api/v1/posts/", где мы можем создавать посты, которые связаны с пользователями и группами
