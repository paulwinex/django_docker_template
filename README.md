
# Django Docker Temlate
Конфигурация для Dodcker-Compose предназначенная для запуска Django проекта

## В шаблоне создаются следующие образы:

- paulwinex/project
    - Исходный образ: python:3.5
- paulwinex/worker
    - Исходный образ: paulwinex/project
- paulwinex/scheduler
    - Исходный образ: paulwinex/project
- paulwinex/nginx
    - Исходный образ: firesh/nginx-lua
- paulwinex/db
    - Исходный образ: postgres:latest
- paulwinex/redis
    - Исходный образ: Redis


## НАСТРОЙКИ

Настройка проекта делается в через мееременные в файле .env

Обязательные настройки:

- NGINX_SERVER - доменное имя
- DJANGO_SETTINGS_MODULE - имя модуля settigs для приложения

Необязательные настройки:

- POSTGRES_DB - имя базы данных 
- POSTGRES_USER - юзер для базы данных
- POSTGRES_PASSWORD - пароль базы данных
- POSTGRES_DATA - дериктория для хранения базы данных
- POSTRGES_BACKUPS - дериктория для резервных копий базы
- POSTGRES_PORT - порт базы данных
- LOG_DIR - папка для логов
- MEDIA_DIR - папка для загружаемых файлов из приложения
- APP_PORT - порт на котором работает приложение

При первом запуске postgres будет создана база данных и пользователь на основе указанных переменных

## ПРОЕКТ

Проект Django находится в папке project
В файле settings.py или local_settings.py для настройки базы данных используйте переменные из os.environ (см. дефолтный проект)
Так же есть возможность запускать проект вне Docker на другой базе даных. Пример также в settings.py. Для определения контекста можно использовать переменную IS_DOCKER_CONTAINER

### TODO:

- добавить задания для cron, бекап базы данных и тп
- добавить сервис daphne (для channels)
- переопределить пути логов для nginx
- добавить HAProxy

# Запуск

### docker install
sudo curl -sSL https://get.docker.com/ | sh

### sudo systemctl status docker
sudo usermod -aG docker $(whoami)

### docker compose
sudo apt-get -y install python-pip git
sudo pip install docker-compose

### скачать проект
cd ~
git clone ...
cd ~/django_docker_example

### Создание образов
./_build_all.sh

### Запуск
docker-compose up -d

### Или
./start_all.sh


# ПОЛЕЗНЫЕ КОМАНДЫ


### Полное пересоздание образов
#### (Нужно находиться в папке с файлом docker-compose.yml)
docker-compose build --no-cache

### Остановка стека
#### (Нужно находиться в папке с файлом docker-compose.yml)
docker-compose down

### Удаление всех остановленных контейнеров
docker rm $(docker ps -a -q -f status=exited)

### Удаление всех контейнеров
docker rm -f $(docker ps -a -q)

### Рестарт всех контейнеров
docker stop $(docker ps -aq);docker start $(docker ps -aq)
#### или
docker-compose restart

### Удаление всех контейнеров
docker stop $(docker ps -aq);docker rm $(docker ps -aq)
### или
docker-compose rm --all -f

### Удаление всех неактивных контейнеров:
docker stop $(docker ps -a | grep 'Exited' | awk '{print $1}') && docker rm $(docker ps -a | grep 'Exited' | awk '{print $1}')

### Удаление всех томов (занятые не удляются) 
docker volume rm $(docker volume ls -q);

### Удаление всех образов (занятые не удляются) 
docker rmi $(docker images -q);

### Как задать количество воркеров?
docker-compose scale worker=3
