from django.test import TestCase
from django.urls import reverse, resolve
from project.views import *

class testurl(TestCase):
    def test_login(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, user_login)
    

    def test_logout(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, user_login)
    

    def test_register(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, user_register)
    

    def test_pass_reset_mail(self):
        url = reverse('pass_reset_mail')
        self.assertEqual(resolve(url).func, pass_reset_mail)


    def test_pass_reset_code(self):
        url = reverse('pass_reset_code')
        self.assertEqual(resolve(url).func, pass_reset_code)


    def test_home(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)


    def test_orders(self):
        url = reverse('orders')
        self.assertEqual(resolve(url).func, orders)


    def test_createorder(self):
        url = reverse('createorder')
        self.assertEqual(resolve(url).func, createorder)


    def test_tasks(self):
        url = reverse('tasks')
        self.assertEqual(resolve(url).func, tasks)


    def test_createtask(self):
        url = reverse('createtask')
        self.assertEqual(resolve(url).func, createtask)    


def test_warehouse(self):
        url = reverse('warehouse')
        self.assertEqual(resolve(url).func, warehouse)    


def test_price(self):
        url = reverse('price')
        self.assertEqual(resolve(url).func, price)    


def test_createwarehouse(self):
        url = reverse('createwarehouse')
        self.assertEqual(resolve(url).func, createwarehouse)    
