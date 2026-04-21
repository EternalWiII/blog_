# Django Blog 

Блог на Django 5 + PostgreSQL.

## Функціонал

- Реєстрація / вхід / вихід (вхід через email)
- Скидання паролю через email
- Профіль користувача (аватар, біо, локація, сайт)
- Створення / редагування / видалення постів
- Статуси постів: Чернетка / Опубліковано
- Теги для постів
- Коментарі до постів
- Пошук по постах
- Пагінація
- Панель адміністратора

## Структура проєкту

```
blog_project/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/          # Авторизація, профіль
│   ├── models.py      # CustomUser, Profile
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── signals.py     # Автостворення Profile
├── blog/              # Пости, коментарі, теги
│   ├── models.py      # Post, Comment, Tag
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/
│   ├── base/base.html
│   ├── blog/
│   └── accounts/
├── static/
├── media/
├── manage.py
└── requirements.txt
```

## Швидкий старт

### 1. Клонуйте та встановіть залежності

```bash
cd blog_project
python -m venv venv
source venv/bin/activate        # Linux/Mac
# або: venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### 2. Налаштуйте змінні середовища

```bash
cp .env.example .env
# Відредагуйте .env — вкажіть свої дані БД та email, SECRET_KEY
```

### 3. Створіть базу даних PostgreSQL

```sql
CREATE DATABASE blog_db;
CREATE USER blog_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE blog_db TO blog_user;

-- найпростіше, але якщо так не хочеться, то можна з правами доступу погратися, щоб все було більш безпечно
GRANT ALL ON SCHEMA public TO blog_user;
GRANT ALL PRIVILEGES ON DATABASE blog_db TO blog_user;
ALTER SCHEMA public OWNER TO blog_user;
```

### 4. Застосуйте міграції

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Запустіть сервер

```bash
python manage.py runserver
```

Відкрийте http://127.0.0.1:8000

## Routing

| URL | Опис |
|-----|------|
| `/` | Список постів |
| `/create/` | Створити пост |
| `/my-posts/` | Мої пости |
| `/<year>/<month>/<day>/<slug>/` | Деталь посту |
| `/tag/<slug>/` | Пости за тегом |
| `/accounts/register/` | Реєстрація |
| `/accounts/login/` | Вхід |
| `/accounts/profile/<username>/` | Профіль |
| `/accounts/profile/edit/me/` | Редагувати профіль |
| `/accounts/password-reset/` | Скидання паролю |
