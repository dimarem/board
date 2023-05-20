# Доска объявлений

Доступ к админке:

* пользователь: **admin**
* пароль: **password**

В корне проекта необходимо создать файл **.env** с двумя переменными:

* EMAIL_HOST_USER - имя пользователя используемой почты
* EMAIL_HOST_PASSWORD - пароль от почты

Зависимости:

* [django](https://www.djangoproject.com)
* [TinyMCE](https://django-tinymce.readthedocs.io/en/latest/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [django-filter](https://django-filter.readthedocs.io/en/stable/)

Установка зависимостей:
```commandline
pip install django
pip install django-tinymce
pip install django-dotenv
pip install django-filter
```
