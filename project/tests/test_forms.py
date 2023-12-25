from django.test import TestCase
from project.forms import *
from project.models import User,Order
from datetime import datetime

class formtest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.order = Order.objects.create(name='zamowienie',
            description='opis',
            client='klient',
            adress='adres',
            state='tw',)
        

    def test_isorder(self):
        form = orderform(data={
            'name': 'zamowienie',
            'description': 'opis',
            'client': 'klient',
            'adress': 'adres',
            'state': 'tw',
        })
        self.assertTrue(form.is_valid())

    def test_noorder(self):
        form = orderform(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


    def test_istask(self):
        form = taskform(data={
            'name': 'zamowienie',
            'user': self.user.id,
            'order': self.order.id,
            'dates': datetime.now(),
        })
        self.assertTrue(form.is_valid())

    def test_notask(self):
        form = taskform(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)


    def test_ismaterial(self):
        form = warehouseform(data={
            'name': 'deska',
            'amount': 10,
        })
        self.assertTrue(form.is_valid())

    def test_nomaterial(self):
        form = warehouseform(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)