import sys
sys.path.append("..")

import unittest

from app import app, db
from app.models import User

class BaseTestCase(unittest.TestCase):
    def setUp(self): 
        app.config.from_object("config.ProductionConfig")
        app.config["WTF_CSRF_ENABLED"]=False

        self.app = app.test_client()
        self.db = db
        self.db.create_all() 

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

class ConfigUnitTests(BaseTestCase):  
    def test_config(self): 
        self.assertFalse(app.config["WTF_CSRF_ENABLED"])
        self.assertFalse(app.config["DEVELOPMENT"])
        self.assertFalse(app.config["DEBUG"])
        self.assertEqual(app.config["DB_NAME"], "prod_database.db")
        self.assertIsNotNone(app.config["SECRET_KEY"])