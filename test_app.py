import unittest
import json
from app import app

class XplorTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        \"\"\"Test if the home page loads successfully.\"\"\"
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_generate_invalid_destination(self):
        \"\"\"Test edge case: Empty destination should return 400.\"\"\"
        response = self.app.post('/api/generate', 
                                 data=json.dumps({'destination': ''}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_generate_invalid_dates(self):
        \"\"\"Test edge case: End date before start date should return 400.\"\"\"
        response = self.app.post('/api/generate', 
                                 data=json.dumps({
                                     'destination': 'Paris',
                                     'start_date': '2026-06-10',
                                     'end_date': '2026-06-05'
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chat_concierge(self):
        \"\"\"Test if TripBot chat endpoint responds.\"\"\"
        response = self.app.post('/api/chat', 
                                 data=json.dumps({'message': 'Hello', 'destination': 'Paris'}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('response', data)

if __name__ == '__main__':
    unittest.main()
