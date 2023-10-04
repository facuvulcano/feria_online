from flask import Flask
from feria.extensions import db, bcrypt, mail, migrate
from feria.routes.main_routes import main_routes
from feria.routes.admin_routes import admin_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object('feria.config')
    app.config.from_pyfile('instance/config.py', silent=True)
    
    # Inicializa las extensiones con la app
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Importa y registra los blueprints
    app.register_blueprint(main_routes)
    app.register_blueprint(admin_routes, url_prefix='')

    return app
