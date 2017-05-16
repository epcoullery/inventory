from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import OrderForm
from .models import Room, Storage, Material, Quantity, Movement, Order, Person, Provider


class InventoryTests(TestCase):
    def setUp(self):
        user = User.objects.create_user('john', 'john@example.org', 'johnpw')
        user.is_staff=True
        user.save()
        self.pers = Person.objects.create(user=user, first_name="John", last_name="Doe")
        self.room = Room.objects.create(number='1', name='Main')
        self.storage = Storage.objects.create(code='st1', room=self.room)
        self.mat1 = Material.objects.create(code="mat1", description="Test mat", unit='box', threshold=1)
        Quantity.objects.create(material=self.mat1, storage=self.storage, quantity=2, price=Decimal('1.50'))

    def test_storage_display(self):
        self.client.login(username='john', password='johnpw')
        response = self.client.get(reverse('storage', args=[self.storage.pk]))
        self.assertContains(response, '<b>st1</b>')

    def test_storage_export(self):
        self.client.login(username='john', password='johnpw')
        response = self.client.get(reverse('storage_export', args=[self.storage.pk]))
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename=exportation_st1_'))

    def test_create_movement_plus(self):
        Movement.objects.create(author=self.pers, typ='order', when=datetime.now(),
            material=self.mat1, storage=self.storage, quantity=1)
        self.assertEqual(Quantity.objects.get(material=self.mat1).quantity, 3)

    def test_create_movement_minus(self):
        Movement.objects.create(author=self.pers, typ='order', when=datetime.now(),
            material=self.mat1, storage=self.storage, quantity=-1)
        self.assertEqual(Quantity.objects.get(material=self.mat1).quantity, 1)

    def test_movement_export(self):
        now = datetime.now()
        Movement.objects.create(author=self.pers, typ='order', when=now,
            material=self.mat1, storage=self.storage, quantity=1)
        self.client.login(username='john', password='johnpw')
        response = self.client.get(reverse('movement_export', args=[now.year]))
        self.assertEqual(response['Content-Disposition'], 'attachment; filename=mouvements_%d.xlsx' % now.year)

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
