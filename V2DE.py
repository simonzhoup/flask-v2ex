from v2de import create_app,db
from flask_script import Manager,Shell
from flask_migrate import Migrate,MigrateCommand

#!/usr/bin/env python
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='v2de/*')
    COV.start()

app = create_app('development')

manager = Manager(app)

migrate = Migrate(app,db)



# def make_shell_context():
#     return dict(app=app, db=db, Tag=Tag, Node=Node)
# manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db',MigrateCommand)

@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


if __name__ == '__main__':
    manager.run()