## Интерент-магазин на Django REST framework

---

### Инструкция по установке:

1. Необходимо скопировать все содержимое репозитория
2. Установить зависимости
```
pip install -r requirements.txt
```
3. Можно воспользоваться имеющейся базой с тестовыми данными или создать новую
```
python manage.py migrate
```
4. Создать суперпользователя (в тестовой базе логин и пароль admin)
``` 
python manage.py createsuperuser
```
5. Создать варианты доставки
``` 
python manage.py make_delivery_types
```
6. Остальные данные можно добавить в админ панели (http://127.0.0.1:8000/admin/)
7. Для запуска сервера используется команда
``` 
python manage.py runserver
```
