from v2de import create_app,db
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand
from v2de.models import Tag,Node

app = create_app('development')

manager = Manager(app)

migrate = Migrate(app,db)

# def make_shell_context():
#     return dict(app=app, db=db, Tag=Tag, Node=Node)
# manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()