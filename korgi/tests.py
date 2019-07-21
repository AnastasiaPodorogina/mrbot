import json

from django.test import TestCase
from django.test import Client
# Create your tests here.
from django.urls import reverse


class TestRegister(TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        # Очистка после каждого метода
        pass

    def test_reg_ok(self):
        url = reverse('registration')
        data_dict = {"username": "", "password": "1234"}
        response = self.client.post(url, json.dumps(data_dict), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def