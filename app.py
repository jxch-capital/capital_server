from flask import Flask
from routes import routes
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

for route in routes:
    app.register_blueprint(route)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello Capital!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
