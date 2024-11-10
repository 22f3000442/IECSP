from flask import Flask
from backend.config import LocalDevelopmentConfig
from backend.models import db, User, Role
from backend.resources import api
from flask_security import Security, SQLAlchemyUserDatastore, auth_required


def createApp():
    app = Flask(__name__, static_folder='frontend', static_url_path = '/static', template_folder ='frontend')
    app.config.from_object(LocalDevelopmentConfig)
    
    db.init_app(app)
    api.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore = datastore, register_blueprint= False)
    app.app_context().push()
    return app

app = createApp()

import backend.create_initial_data

import backend.routes

if (__name__ == '__main__'):
    app.run(debug = True)
    
