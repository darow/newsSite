from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


def create_user(username='test_user', password='default_pass'):
    user = User.objects.create_user(username=username, password=password)
    return user


class AuthenticationFormTest(TestCase):
    def test_LoginForm_still_AuthenticationForm(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'], AuthenticationForm)

    def test_LoginForm_valid(self):
        form = AuthenticationForm(data={'username': 'test_user', 'password': 'default_pass'})
        self.assertEqual(form.is_valid(), False)

    def test_LoginForm_valid(self):
        create_user()
        form = AuthenticationForm(data={'username': 'test_user', 'password': 'default_pass'})
        self.assertEqual(form.is_valid(), True)


