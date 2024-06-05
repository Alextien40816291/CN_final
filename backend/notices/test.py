from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123456')

    def test_login_valid_user(self):
        response = self.login(username='admin', password='123456')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_invalid_user(self):
        response = self.login(username='wronguser', password='wrongpass')
        self.assertFalse(response.context['user'].is_authenticated)

    def login(self, username, password):
        return self.client.post(reverse('login'), {'username': username, 'password': password})

