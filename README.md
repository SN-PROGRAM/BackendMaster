BackendMaster — это образовательная платформа, разработанная на Django, предназначенная для изучения backend-программирования. Проект включает в себя модули курсов, систему заданий и управление пользователями. Он разрабатывается с прицелом на качественный обучающий контент, модульную архитектуру и удобную поддержку новых функциональностей.

**Установка проекта**

1. Клонируйте репозиторий

git clone https://github.com/SN-PROGRAM/BackendMaster

cd BackendMaster

2. Создайте и активируйте виртуальное окружение

Windows:

python -m venv .venv
.\.venv\Scripts\activate

MacOS/Linux:

python3 -m venv .venv
source .venv/bin/activate

3. Установите зависимости

pip install -r requirements.txt

4. Примените миграции

python manage.py makemigrations
python manage.py migrate

5. Создайте суперпользователя

python manage.py createsuperuser

6. Запустите сервер

python manage.py runserver

**Структура проекта**

BackendMaster/ — конфигурации Django-проекта

courses/ — приложение с курсами

tasks/ — приложение с задачами

users/ — приложение с пользователями

static/ — директория для статики

manage.py — управляющий файл Django

requirements.txt — список зависимостей

README.md — документация проекта

.gitignore — исключения для Git

.venv/ — виртуальное окружение

**Полезные команды при разработке**

1) Запуск сервера:

python manage.py runserver

2) Применение миграций:

python manage.py migrate

3) Создание миграций:

python manage.py makemigrations

4) Создание суперпользователя:

python manage.py createsuperuser

**Работа с Git**

1) Создание новой ветки:

git checkout -b имя-ветки

2) Отправка своей ветки на GitHub:

git push origin имя-ветки

3) Переход на основную ветку:

git checkout main

4) Получение актуальной версии основной ветки:

git pull origin main

5) Слияние своей ветки в основную:

git checkout main

git pull origin main

git merge имя-ветки

git push origin main

Дополнительные рекомендации:

1. Все изменения вносятся через отдельные ветки.
 
2. Перед созданием Pull Request убедитесь в отсутствии конфликтов.
 
3. Обновляйте requirements.txt, если добавляете библиотеки.
 
4. Описание коммитов должно быть осмысленным и отражать суть изменений.
