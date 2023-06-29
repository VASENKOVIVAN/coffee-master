# для определения таблицы и модели
from sqlalchemy.ext.declarative import declarative_base

# для настроек
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# создание экземпляра declarative_base
Base = declarative_base()
# Подключаемся и создаем сессию базы данных
engine = create_engine('mysql+pymysql://root:change-me@localhost/devopsroles')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from application.user.userModel import *


# def init_db():
#     # Здесь нужно импортировать все модули, где могут быть определены модели,
#     # которые необходимым образом могут зарегистрироваться в метаданных.
#     # В противном случае их нужно будет импортировать до вызова init_db()
#     import application.user.userModel
#     Base.metadata.create_all(bind=engine)


# # создает экземпляр create_engine в конце файла
# engine = create_engine('mysql+pymysql://root:change-me@localhost/devopsroles')

Base.metadata.create_all(engine)

