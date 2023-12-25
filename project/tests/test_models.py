from django.test import TestCase
from project.models import User, Warehouse, Order, Task

class UserModelTest(TestCase):

    def test_create_user(self):
        user = User.objects.create(
            email='test@.com',
            username='test',
            first_name='imie',
            last_name='nazwisko',
            role=User.WORKER
        )

        self.assertEqual(user.email, 'test@.com')
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.first_name, 'imie')
        self.assertEqual(user.last_name, 'nazwisko')
        self.assertEqual(user.role, User.WORKER)

class WarehouseModelTest(TestCase):

    def test_create_warehouse(self):
        warehouse = Warehouse.objects.create(
            name='material',
            amount=50.0
        )

        self.assertEqual(warehouse.name, 'material')
        self.assertEqual(warehouse.amount, 50.0)


class OrderModelTest(TestCase):

    def test_create_order(self):
        order = Order.objects.create(
            name='zamowienie',
            description='opis',
            client='klient',
            adress='adres',
            state='tw',
            assessed=100.0,
        )

        self.assertEqual(order.name, 'zamowienie')
        self.assertEqual(order.description, 'opis')
        self.assertEqual(order.client, 'klient')
        self.assertEqual(order.adress, 'adres')
        self.assertEqual(order.state, 'tw')
        self.assertEqual(order.assessed, 100.0)


class TaskModelTest(TestCase):

    def test_create_task(self):
        user = User.objects.create(
            email='test@example.com',
            username='testuser',
            first_name='John',
            last_name='Doe',
        )
        order = Order.objects.create(
            name='zamowienie',
            description='opis',
            client='klient',
            adress='adres',
            state='tw',
            assessed=100.0,
        )
        task = Task.objects.create(
            name='zadanie',
            user=user,
            order=order,
            dates='2023-12-31 12:00:00',
        )

        self.assertEqual(task.name, 'zadanie')
        self.assertEqual(task.user, user)
        self.assertEqual(task.order, order)
        self.assertEqual(str(task.dates), '2023-12-31 12:00:00')
