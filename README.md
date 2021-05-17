# ida_test

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver 8000
http://127.0.0.1:8000

# Добавление
Принимаются только прямые ссылки на изображения без защиты от ботов.

# Изменение размера
Изображение меняется только в меньшую сторону. Для сохранения пропорций из переданых высоты и шырины выбирается меньшее.
