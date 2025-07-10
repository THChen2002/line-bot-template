from flask import Flask, render_template
from linebot_app import linebot_app
from liff_app import liff_app
from admin_app import admin_app
from config import get_config

config = get_config()
firebaseservice = config.firebaseService

app = Flask(__name__)
app.register_blueprint(linebot_app)
app.register_blueprint(liff_app, url_prefix='/liff')
app.register_blueprint(admin_app, url_prefix='/admin')

@app.route('/')
def index():
    return render_template('app/index.html')

@app.route('/forbidden', methods=['GET'])
def forbidden_page():
    return render_template('http/forbidden.html')

if __name__ == "__main__":
    app.run()