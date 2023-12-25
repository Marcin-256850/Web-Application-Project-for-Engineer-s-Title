from django.test import TestCase, Client
from django.urls import reverse
from project.models import User


class testview(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@.com',
            password='testpassword',
            role='wl'
        )
         

    def test_user_login(self):
        client = Client()
        response = client.post(reverse('login'), {'mail': 'test@.com', 'passw': 'testpassword', 'role': 'wl'})
        self.assertEqual(response.status_code, 302)


    def test_user_logout(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

        
    def test_home_view(self):
        client = Client()
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)