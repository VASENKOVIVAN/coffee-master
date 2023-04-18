from sqlalchemy import Column, Boolean, Integer, String, DateTime
from database_setup import Base
from datetime import datetime
from marshmallow import fields, Schema
print('fdjhskljhflkhdslkghfldskjgflksdjgfpoikjgbol')
class User(Base):
    """User Model"""
    __tablename__ = 'user'
    _id = Column('_id', Integer, primary_key=True)
    login = Column('login', String(250), nullable=False)
    password = Column('password', String(255), nullable=False)
    active = Column('active', Boolean(), default=True)
    created_on = Column('created_on', DateTime(), default=datetime.now)

    # def __init__(self, login='123', password='123', active=True, created_on=''):
    #     self.login = login
    #     self.password = password
    #     self.active = active
    #     self.created_on = created_on



class UserSchema(Schema):
    """Schema to retrieve data from Model Discount Type as dictionary.
    data_key is an alias for column name."""
    _id=fields.Int(data_key='_id')
    login=fields.Str(data_key='login')
    password=fields.Str(data_key='password')
    active=fields.Bool(data_key='active')
    created_on=fields.Str(data_key='created_on')