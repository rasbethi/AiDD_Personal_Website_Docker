import unittest
from app import app

class FlaskRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        print("Home page loaded successfully")

    def test_contact_page(self):
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)
        print("Contact page loaded successfully")

if __name__ == "__main__":
    unittest.main()
