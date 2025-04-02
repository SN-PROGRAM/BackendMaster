BackendMaster — это образовательная платформа, разработанная на Django, предназначенная для изучения backend-программирования. Проект включает в себя модули курсов, систему заданий и управление пользователями. Он разрабатывается с прицелом на качественный обучающий контент, модульную архитектуру и удобную поддержку новых функциональностей.

Установка проекта

1. Клонируйте репозиторий

git clone https://github.com/S-NOWNUM-B/BackendMaster.git
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

Структура проекта:

	•	BackendMaster/ — конфигурации Django-проекта

	•	courses/ — приложение с курсами

	•	tasks/ — приложение с задачами

	•	users/ — приложение с пользователями

	•	static/ — директория для статики

	•	manage.py — управляющий файл Django

	•	requirements.txt — список зависимостей

	•	README.md — документация проекта

	•	.gitignore — исключения для Git

	•	.venv/ — виртуальное окружение

Полезные команды при разработке

Запуск сервера:

python manage.py runserver

Применение миграций:

python manage.py migrate

Создание миграций:

python manage.py makemigrations

Создание суперпользователя:

python manage.py createsuperuser

Работа с Git

Создание новой ветки:

git checkout -b имя-ветки

Отправка своей ветки на GitHub:

git push origin имя-ветки

Переход на основную ветку:

git checkout main

Получение актуальной версии основной ветки:

git pull origin main

Слияние своей ветки в основную:

git checkout main
git pull origin main
git merge имя-ветки
git push origin main

Дополнительные рекомендации
	•	Все изменения вносятся через отдельные ветки.
	•	Перед созданием Pull Request убедитесь в отсутствии конфликтов.
	•	Обновляйте requirements.txt, если добавляете библиотеки.
	•	Описание коммитов должно быть осмысленным и отражать суть изменений.