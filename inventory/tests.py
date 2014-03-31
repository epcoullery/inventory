# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from decimal import Decimal

from django.test import TestCase

from .models import Room, Storage, Material, Quantity, Movement, Person


class InventoryTests(TestCase):
    def setUp(self):
        self.pers = Person.objects.create(first_name="John", last_name="Doe")
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
