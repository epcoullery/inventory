# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db import transaction


class Material(models.Model):
    code = models.CharField(max_length=100)
    description = models.TextField()
    unit = models.CharField("Unité", max_length=20)
    threshold = models.SmallIntegerField("Seuil de commande", default=0)

    class Meta:
        verbose_name = "Matériel"

    def __unicode__(self):
        return self.description


class Room(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Salle"
        ordering = ('number',)

    def __unicode__(self):
        return "%s —­ %s" % (self.number, self.name)


class Storage(models.Model):
    code = models.CharField(max_length=100)
    room = models.ForeignKey(Room)
    materials = models.ManyToManyField(Material, through='Quantity')

    class Meta:
        verbose_name = "Armoire"

    def __unicode__(self):
        return "%s (%s)" % (self.code, self.room)

    def get_absolute_url(self):
        return reverse('storage', args=[self.pk])


class Quantity(models.Model):
    material = models.ForeignKey(Material)
    storage = models.ForeignKey(Storage)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Prix à l'unité")

    class Meta:
        verbose_name = "Quantité"
        unique_together = ("material", "storage")

    def __unicode__(self):
        return "%d %s (stored in %s)" % (self.quantity, self.material, self.storage)


class Person(models.Model):
    user = models.OneToOneField(User, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    initials = models.CharField(max_length=5, blank=True, default='')

    class Meta:
        verbose_name = "Personnel"
        ordering = ('last_name',)

    def __unicode__(self):
        return "%s %s" % (self.last_name, self.first_name)


MOVEMENT_TYPES = (
    ('init', "Approvisionnement initial"),
    ('order', "Commande"),
    ('fix', "Correction (perte, inventaire)"),
    ('use', "Prélèvement"),
    ('borrow', "Emprunt"),
    ('back', "Retour"),
    ('transfer', "Transfert"),
)
class Movement(models.Model):
    author = models.ForeignKey(Person)
    typ = models.CharField(max_length=20, choices=MOVEMENT_TYPES, verbose_name="Opération")
    when = models.DateTimeField()
    material = models.ForeignKey(Material)
    storage = models.ForeignKey(Storage)
    quantity = models.IntegerField()
    comment = models.TextField(default='', blank=True, verbose_name="Commentaire")

    class Meta:
        verbose_name = "Mouvement"

    def __unicode__(self):
        return "On %s: %d of %s in %s by %s" % (
            self.when, self.quantity, self.material, self.storage, self.author)

    def save(self, *args, **kwargs):
        # Updated stored quantity when movement saved
        with transaction.atomic():
            super(Movement, self).save(*args, **kwargs)
            quant, _ = Quantity.objects.get_or_create(material=self.material, storage=self.storage,
                defaults={'quantity': 0, 'price': Decimal('0.0')})
            quant.quantity += self.quantity
            quant.save()


class Provider(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    npa = models.CharField(max_length=5)
    locality = models.CharField(max_length=50)
    country = models.CharField(max_length=50, default='Suisse')
    phone = models.CharField(max_length=20, blank=True, default='')
    fax = models.CharField(max_length=20, blank=True, default='')
    email = models.CharField(max_length=100, blank=True, default='')
    web = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        verbose_name = "Fournisseur"
        ordering = ('name',)

    def __unicode__(self):
        return self.name


class Order(models.Model):
    order_date = models.DateField("Date de commande")
    receive_date = models.DateField("Date de réception", blank=True, null=True)
    provider = models.ForeignKey(Provider, verbose_name="Fournisseur")
    material = models.ForeignKey(Material, verbose_name="Matériel")
    quantity = models.PositiveIntegerField("Quantité")
    price = models.DecimalField("Prix", max_digits=8, decimal_places=2,
        blank=True, null=True, help_text="Prix à l'unité")

    class Meta:
        verbose_name = "Commande"

    def __unicode__(self):
        return "On %s: %d of %s" % (self.order_date, self.quantity, self.material)
