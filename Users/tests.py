# Create your tests here.
import django
from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model, SESSION_KEY
from django.urls import reverse

CLIENT_EMAIL = 'testclient@example.com'
STAFF_EMAIL = 'staffmember@example.com'
PASSWORD = 'password'


class UsersManagersTests(TestCase):

    def test_create_user(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(email='test@user.com', password=PASSWORD)
        self.assertEqual(user.email, 'test@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            user_model.objects.create_user()
        with self.assertRaises(TypeError):
            user_model.objects.create_user(email='')
        with self.assertRaises(ValueError):
            user_model.objects.create_user(email='', password=PASSWORD)

    def test_create_staff_user(self):
        user_model = get_user_model()
        user = user_model.objects._create_user(email='test2@user.com', password=PASSWORD, is_staff=True,
                                               is_superuser=False)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.email, 'test2@user.com')

    def test_create_super_user(self):
        user_model = get_user_model()
        user = user_model.objects._create_user(email='test3@user.com', password=PASSWORD, is_staff=True,
                                               is_superuser=True)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email, 'test3@user.com')


class AuthViewsTestCase(TestCase):
    """
    Helper base class for all the follow test cases.
    """

    @classmethod
    def setUpTestData(cls):
        cls.u1 = get_user_model().objects.create_user(password=PASSWORD, email=CLIENT_EMAIL)
        cls.u3 = get_user_model().objects.create_user(password=PASSWORD, email=STAFF_EMAIL)

    def test_login(self, email=CLIENT_EMAIL, password=PASSWORD):
        response = self.client.post('/accounts/login/', {
            CLIENT_EMAIL: email,
            PASSWORD: password,
        })
        # self.assertIn(SESSION_KEY, self.client.session)
        self.assertEqual(response.status_code, 200)
        return response

    def test_logout(self, email=CLIENT_EMAIL, password=PASSWORD):
        response = self.client.post('/accounts/login/', {
            CLIENT_EMAIL: email,
            PASSWORD: password,
        })
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/accounts/logout/')
        print(response)
        # self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/accounts/login', fetch_redirect_response=False)
        # self.assertNotIn(SESSION_KEY, self.client.session)
