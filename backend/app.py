from flask import Flask

# для определения таблицы и модели
# from sqlalchemy.ext.declarative import declarative_base
# # для создания отношений между таблицами
# from sqlalchemy.orm import relationship
# # для настроек
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from flask_cors import CORS

app = Flask(__name__)

CORS(app)
# # создание экземпляра declarative_base
# Base = declarative_base()
# # Подключаемся и создаем сессию базы данных
# engine = create_engine('mysql+pymysql://root:change-me@localhost/devopsroles')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
# # создает экземпляр create_engine в конце файла
# engine = create_engine('mysql+pymysql://root:change-me@localhost/devopsroles')
# Base.metadata.create_all(engine)


# JWT_SECRETKEY=bcrypt.hashpw(b'itsAs3cr34tkeyforJWT', bcrypt.gensalt())
# JWT_SECRETKEY='this is a secret'

# SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
# print(SECRET_KEY)
# app.config['SECRET_KEY'] = SECRET_KEY