[![foodgram workflow](https://github.com/TimRock23/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/TimRock23/foodgram-project/actions/workflows/foodgram_workflow.yml)

# **FoodGram**
***
Онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на 
публикации других пользователей, добавлять понравившиеся рецепты в список 
«Избранное», а перед походом в магазин скачивать сводный список продуктов, 
необходимых для приготовления одного или нескольких выбранных блюд.
***

## Запуск проекта (Docker)
1. Запустить docker-compose:

`docker-compose up`

2. Чтобы загрузить список ингредиентов в БД:

`docker-compose exec web python manage.py loaddata fixtures.json`

3. Для создания суперпользователя введите следующую команду:

`docker-compose exec web python manage.py createsuperuser`

***
## **Технологии**
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Nginx](https://nginx.org/)
- [Gunicorn](https://gunicorn.org/)
- [Docker](https://www.docker.com/)
- [Яндекс Облако](https://cloud.yandex.ru/)
- [GitHub Actions](https://github.com/features/actions)
