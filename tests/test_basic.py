import unittest
from app import create_app, db

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_main_page(self):
        # We add the /api prefix here to match your __init__.py config
        response = self.client.get('/api/marhaba') 
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()