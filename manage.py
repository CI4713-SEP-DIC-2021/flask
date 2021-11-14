import os
from flask_script import Manager,  Server
from flask_migrate import Migrate, MigrateCommand
from settings.environment import APP_SETTINGS

from app import app, db

app.config.from_object(APP_SETTINGS)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=8000))

if __name__ == '__main__':
    manager.run()