from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser, Profile


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')

    def test_register_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.get(email='test@example.com')
        self.assertEqual(user.username, 'testuser')

    def test_profile_auto_created(self):
        self.client.post(self.register_url, {
            'username': 'testuser2',
            'email': 'test2@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        user = CustomUser.objects.get(email='test2@example.com')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)

    def test_duplicate_email_rejected(self):
        CustomUser.objects.create_user(
            username='existing', email='exist@example.com', password='Pass123!'
        )
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'exist@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(CustomUser.objects.count(), 1)


class UserLoginTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='StrongPass123!'
        )
        self.login_url = reverse('accounts:login')

    def test_login_page_loads(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('blog:post_list'))

    def test_wrong_password_rejected(self):
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser', email='test@example.com', password='StrongPass123!'
        )

    def test_profile_page_loads(self):
        response = self.client.get(reverse('accounts:profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)

    def test_profile_edit_requires_login(self):
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit_accessible_when_logged_in(self):
        self.client.login(username='test@example.com', password='StrongPass123!')
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 200)
