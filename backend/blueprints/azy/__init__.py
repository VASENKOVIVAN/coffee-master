from flask import Blueprint
from flask_restx import Api
from blueprints.azy.primery_api import namespace as primery_api_ns

blueprint = Blueprint('swagger', __name__, url_prefix='/swagger')

api_extension = Api(
    blueprint,
    title='Swagger Coffee-Master 1.0',
    version='1.0',
    description='Инструкция к приложению для <b>статьи по Flask REST API\
    </b>, демонстрирующему возможности <b>пакета RESTX</b>, позволяющему\
    создавать масштабируемые сервисы и генерировать API документацию по ним',
    doc='/doc',
    url='https://petstore3.swagger.io/api/v3',
    servers='https://petstore3.swagger.io/api/v3'
)

api_extension.add_namespace(primery_api_ns)