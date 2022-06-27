# API для проекта YaMDb

  Проект YaMDb собирает отзывы пользователей на произведения.
  Произведения разделены на категории.
  Произведениям может быть присвоен жанр.
  Произведению можно выставить оценку (1-10), на базе оценок пользователей формируется рейтинг произведений.
  
## Возможности

#### Регистрация пользователя

 - Регистрация пользователя с передачей username и адреса электронной почты сервису
 - Получение пользователем confirmation code на электронную почту
 - Получение токена для использования сервиса в обмен на username и код подтверждения

#### Работа с категориями

 - Получение списка имеющихся категорий
 - Добавление категории администратором
 - Удаление категории администратором

#### Работа с жанрами

 - Получение списка имеющихся канров
 - Добавление жанра администратором
 - Удаление жанра администратором

#### Работа с произведениями

 - Получение списка всех произведений
 - Добавление произведения администратором
 - Информация о конкретном произведении
 - Частичное обновление информации о произведении администратором
 - Удаление произведения администратором

#### Работа с отзывами

 - Получение списка всех отзывов на произведение
 - Добавление нового отзыва авторизованным пользователем
 - Получение конкретного отзыва произведения
 - Частичное обновление отзыва автором/модератором/администратором
 - Удаление отзыва автором/модератором/администратором

#### Работа с комментариями к отзывам

 - Получение списка всех комментариев к отзыву
 - Добавление комментария к отзыву авторизованным пользователем
 - Получение конкретного комментария к отзыву
 - Частичное обновление комментария к отзыву автором/модератором/администратором
 - Удаление комментария к отзыву автором/модератором/администратором

#### Работа с пользователями

 - Получение списка всех пользователей администратором
 - Добавление пользователя администратором (пользователь получает код подтверждения на электронную почту и завершает регистрацию самостоятельно)
 - Получение информации о конкретном пользователе администратором
 - Изменение данных пользователя администратором
 - Удаление пользователя администратором
 - Получение данных своей учетной записи авторизованным пользователем
 - Частичное изменение данных своей учетной записи авторизованным пользователем

## Установка

*Для работы с проектом в системе должен быть установлен Python версии 3.7*

### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/eduvxn/api_yamdb.git
```

```
cd api_yamdb

```

### Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

#### команда для Linux

```
source venv/bin/activate
```

#### команда для windows

```
source venv/Scripts/activate
```
#### Обновить пакетный менежер pip

```
python3 -m pip install --upgrade pip
```

### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

### Выполнить миграции:

```
python3 manage.py migrate
```

### Запустить

```
python3 manage.py runserver
```

## Использование

После запуска сервера вам будет доступна [документация](http://localhost:8000/redoc/)

### Регистрация для пользователей

```bash
POST /api/v1/auth/signup/ - получение кода подтверждения на указанный email
```

в body
{
"email": "string",
"username": "string"
}

###### Использовать имя 'me' в качестве username запрещено

```bash
POST /api/v1/auth/token/ - получение JWT-токена в обмен на username и confirmation code
```

в body
{
"username": "string",
"confirmation_code": "string"
}

### Примеры работы с API для пользователей

Для неавторизованных пользователей работа с API доступна в режиме чтения.

```bash
GET /api/v1/categories/ - получение списка всех категорий

GET /api/v1/genres/ - получение списка всех жанров

GET /api/v1/titles/ - получение списка всех произведений

GET /api/v1/titles/{titles_id}/ - получение информации о произведении по id

GET /api/v1/titles/{title_id}/reviews/ - получение списка всех отзывов по id произведения

GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ - получение списка всех комментариев к отзыву по id произведения и id отзыва

GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ - получение конкретного комментариея к отзыву по id произведения, id отзыва и id комментария
```

### Примеры работы с API для авторизованных пользователей

Добавление отзыва:

```bash
POST /api/v1/titles/{title_id}/reviews/
```

в body
{
"text": "string",
"score": 1
}

Частичное обновление отзыва:

```bash
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/
```

в body
{
"text": "string",
"score": 2
}

Удаление отзыва:

```bash
DEL /api/v1/titles/{title_id}/reviews/{review_id}/
```

Добавление комментария к отзыву:

```bash
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

в body
{
"text": "string"
}

Частичное обновление комментария к отзыву:

```bash
PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

в body
{
"text": "string"
}

Удаление поста:

```bash
DEL /api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
### Остальные примеры работы с сервисом возможно изучить [здесь](http://localhost:8000/redoc/)

## Технологии

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django REST framework](https://www.django-rest-framework.org/)
* [DRF Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)