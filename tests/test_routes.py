import unittest
from app.__main__ import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_all_conversations(self):
        response = self.app.get('/conversation')
        self.assertEqual(response.status_code, 200)

    def test_create_question(self):
        response = self.app.post('/question', json={'question': 'Test question'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
