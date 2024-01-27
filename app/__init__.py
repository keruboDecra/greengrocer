from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
login_manager = LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__, static_folder="statics")
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)

    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.add_url_rule('/', endpoint='index')
    app.register_blueprint(auth_blueprint)

    @app.route('/hello')
    def hello():
        return '<h2>Hello world. This is Green Grocer</h2>'

    @app.errorhandler(500)
    def handle_500(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def handle_404(e):
        return render_template('404.html'), 404
    return app
