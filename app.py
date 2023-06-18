from flask import Flask, jsonify
from routes import routes
import logging
from flask_cors import CORS
from utils.proxy_utils import proxy

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

for route in routes:
    app.register_blueprint(route)

CORS(app, supports_credentials=True)


# if app.debug:
#     proxy('localhost', 10808)

proxy('localhost', 10808)
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello Capital!'


@app.errorhandler(Exception)
def error_handler(e):
    data = {
        "code": -1,
        "msg": str(e),
        "data": None
    }

    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
