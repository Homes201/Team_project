from django.test import TestCase, Client
from bs4 import BeautifulSoup
import json

class AssistantAppTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        bs = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue(bs.find('title'))
        self.assertIn('Welcome', bs.text)

    def test_get_response(self):
        url = '/query/'

        valid_data = {'query': 'Hello, how are you?'}
        valid_response = self.client.post(
            url, 
            data=json.dumps(valid_data), 
            content_type='application/json'
        )
        self.assertEqual(valid_response.status_code, 200)
        self.assertIn('response', valid_response.json())

        # Case 2: Invalid POST request
        invalid_data = {'query': ''}
        invalid_response = self.client.post(
            url, 
            data=json.dumps(invalid_data), 
            content_type='application/json'
        )
        self.assertEqual(invalid_response.status_code, 400)
        self.assertIn('error', invalid_response.json())
