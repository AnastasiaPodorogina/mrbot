import json

from django.test import TestCase
from django.test import Client
# Create your tests here.
from django.urls import reverse

from korgi.models import CustomUser


class TestRegister(TestCase):

    def setUp(self):
        self.client = Client()
        self.custom_user = CustomUser(username='test')
        self.custom_user.set_password('test')
        self.custom_user.save()

    def tearDown(self):
        CustomUser.objects.get(username='test').delete()

    def test_reg_ok(self):
        url = reverse('registration')
        data_dict = {"username": "aa", "password": "1234"}
        response = self.client.post(url, json.dumps(data_dict), content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_login_ok(self):
        url = reverse('login')
        data_dict = {"username": "test", "password": "test"}
        response = self.client.post(url, json.dumps(data_dict), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_count_ok(self):
        url = reverse('login')
        data_dict = {"username": "test", "password": "test"}
        response = self.client.post(url, json.dumps(data_dict), content_type="application/json")
        url = reverse('count')
        response = self.client.get(url)
        self.assertEqual(response.content, b'For user test count = 0')
        response = self.client.post(url)
        self.custom_user = CustomUser.objects.get(username='test')
        self.assertEqual(self.custom_user.count, 1)
        self.assertEqual(response.content, b'Count update 1 for test')
        response = self.client.delete(url)
        self.custom_user = CustomUser.objects.get(username='test')
        self.assertEqual(self.custom_user.count, 0)
        self.assertEqual(response.content, b'Count update 0 for test')
