import unittest
from v2de.models import User,Tag,CollecTag
from v2de import create_app, db
from flask import current_app

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

class TagModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_tag_create(self):
        name='tag'
        name2='tag2'
        t = Tag(name=name)
        db.session.add(t)
        db.session.commit()
        self.assertTrue(Tag.query.filter_by(name=name).first())
        self.assertIsNone(Tag.query.filter_by(name=name2).first())

    def test_collection(self):
        name = ' tag'
        t = Tag(name=name)
        user = User(username='user')
        db.session.add(t)
        db.session.add(user)
        db.session.commit()
        c = CollecTag(tag_id=t.id,user_id=user.id)
        db.session.add(c)
        db.session.commit()
        self.assertTrue(t.collection(user))
        self.assertTrue(t.__repr__()=='<Role %r>' % t.name)
