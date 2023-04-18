# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.9

# Скачиваем/обновляем необходимые библиотеки для проекта 
# COPY requirements.txt /backend
COPY ./requirements.txt /backend/requirements.txt

# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /backend

RUN pip install -r requirements.txt
# RUN pip3 install --upgrade pip -r requirements.txt

# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . /backend
# Устанавливаем порт, который будет использоваться для сервера
EXPOSE 5000

# configure the container to run in an executed manner
ENTRYPOINT ["python"]
CMD ["main.py"]