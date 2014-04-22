# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .forms import OrderForm
from .models import Room, Storage, Material, Quantity, Movement, Order, Person, Provider


class InventoryTests(TestCase):
    def setUp(self):
        self.pers = Person.objects.create(user=User.objects.create(username='john'), first_name="John", last_name="Doe")
        self.room = Room.objects.create(number='1', name='Main')
        self.storage = Storage.objects.create(code='st1', room=self.room)
        self.mat1 = Material.objects.create(code="mat1", description="Test mat", unit='box', threshold=1)
        Quantity.objects.create(material=self.mat1, storage=self.storage, quantity=2, price=Decimal('1.50'))

    def test_create_movement_plus(self):
        Movement.objects.create(author=self.pers, typ='order', when=datetime.now(),
            material=self.mat1, storage=self.storage, quantity=1)
        self.assertEqual(Quantity.objects.get(material=self.mat1).quantity, 3)

    def test_create_movement_minus(self):
        Movement.objects.create(author=self.pers, typ='order', when=datetime.now(),
            material=self.mat1, storage=self.storage, quantity=-1)
        self.assertEqual(Quantity.objects.get(material=self.mat1).quantity, 1)

    def test_total_quantity(self):
        self.assertEqual(self.mat1.total_quantity(), 2)

    def test_receive_order(self):
        """
        Test receiving an order increment quantity on some storage.
        """
        prov = Provider.objects.create(
            name='Food AG', address='Main street', npa='4444', locality='Nowhere')
        order_data = {'order_date': datetime.today(), 'provider': prov, 'material': self.mat1, 'quantity': 3}
        order = Order.objects.create(**order_data)
        self.assertEqual(self.mat1.total_quantity(), 2)
        fake_req = type(str('Request'), (object,), {'user': self.pers.user, 'POST': {'storage': self.storage.pk}})
        order_data.update({
            'receive_date': datetime.today(), 'storage': self.storage.pk, 'provider': prov.pk, 'material': self.mat1.pk
        })
        OrderForm(order_data, instance=order).save(fake_req)
        self.assertEqual(self.mat1.total_quantity(), 5)
