# AuditSRO

Сервис мониторинга финансовых проверок в саморегулируемых организациях.

[Техническое задание](./docs/technical_requirements.md)  
[Схема взаимодействия](./docs/interaction_scheme.md)  
[Планы по развитию](./docs/TODO.md)

___

## Блоки сервиса

1. Верстка находиться в директории `html_pages_layout`.

> <img src="./docs/img/home_page.png"  style="width: 300px" alt="Home page"/>
> <img src="./docs/img/about_page.png"  style="width: 300px" alt="About page"/>

2. Скрапер расположен в директории `scraper`.   
   Для запуска необходимо:
    - установить зависимости из `requirements.txt`;
    - перейти в директорию `scraper`;
    - вызвать паука по имени и передать путь к файлу результатов:

```shell
scrapy crawl naufor -O ../auditsro/naufor.csv
```

3. Backend приложения расположен в директории `auditsro`.
   Для запуска необходимо:
    - установить зависимости из `requirements.txt`;
    - переименовать файл `.env_sample` в `.env` и настроить свои значения переменных окружения;
    - если планируется работа с базой данных через докер, то можно воспользоваться файлом `docker-compose.yml`;

```shell
docker-compose up --build -d --remove-orphans
```

- перейти в директорию `auditsro`;
- ввести команды:

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

- при необходимости можно заполнить базу данных одной из следующих команд:

```shell
python manage.py fake_fill_db
python manage.py fill_db
```
