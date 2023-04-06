from flask import Flask
from routes import routes
import logging
from flask_cors import CORS
from utils.proxy_utils import proxy

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

for route in routes:
    app.register_blueprint(route)

CORS(app, supports_credentials=True)

if app.config['ENV'] == 'development':
    proxy('localhost', 10808)
elif 'FLASK_NEED_PROXY' in app.config and app.config['FLASK_NEED_PROXY']:
    proxy(app.config['FLASK_PROXY_HOST'], app.config['FLASK_PROXY_PORT'])


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello Capital!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
