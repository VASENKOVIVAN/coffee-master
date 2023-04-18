from app import app
from application.user.userController import UserController, LoginController
from application.utilities.auth import Auth
from flask import jsonify, request, make_response

auth=Auth()

@app.route('/api/v1')
@auth.middleware
def hello_world():
    return jsonify({
        "message": "test message auth"
    })


@app.route('/api/v1/test', methods=['GET'])
def hello_worldtest():
    return jsonify({
        "message": "test message nonauth"
    })


@app.route('/api/v1/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    controller=UserController()
    if request.method == 'POST':
        return controller.insertNewData()
    

@app.post('/api/v1/login')
def login():
    return LoginController().login()


@app.get('/api/v1/logout')
def logOut():
    return LoginController().logOut()


@app.route('/q')
def index():
    resp = make_response({
        "message": "q"
    })
    resp.set_cookie('somecookiename', 'I am cookie')
    return resp 


@app.route('/get-cookie/')
def get_cookie():
    username = request.cookies.get('somecookiename')
    return username 


@app.errorhandler(404)
def forbidden(e):
    return jsonify({
        "message": "Endpoint Not Found",
        "error": str(e),
        "data": None
    }), 404