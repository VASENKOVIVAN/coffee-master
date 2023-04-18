# from app import db, migrate
# from app import session


# from migrate import *


# flask run --port=5000


from api import *


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
