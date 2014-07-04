# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('unit', models.CharField(max_length=20, verbose_name='Unit\xe9')),
                ('threshold', models.SmallIntegerField(default=0, verbose_name='Seuil de commande')),
            ],
            options={
                'verbose_name': 'Mat\xe9riel',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typ', models.CharField(max_length=20, verbose_name='Op\xe9ration', choices=[('init', 'Approvisionnement initial'), ('order', 'Commande'), ('fix', 'Correction (perte, inventaire)'), ('use', 'Pr\xe9l\xe8vement'), ('borrow', 'Emprunt'), ('back', 'Retour'), ('transfer', 'Transfert')])),
                ('when', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('comment', models.TextField(default='', verbose_name='Commentaire', blank=True)),
                ('material', models.ForeignKey(to='inventory.Material')),
            ],
            options={
                'verbose_name': 'Mouvement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_date', models.DateField(verbose_name='Date de commande')),
                ('receive_date', models.DateField(null=True, verbose_name='Date de r\xe9ception', blank=True)),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantit\xe9')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, blank=True, help_text="Prix \xe0 l'unit\xe9", null=True, verbose_name='Prix')),
                ('material', models.ForeignKey(verbose_name='Mat\xe9riel', to='inventory.Material')),
            ],
            options={
                'verbose_name': 'Commande',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('initials', models.CharField(default='', max_length=5, blank=True)),
                ('user', models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('last_name',),
                'verbose_name': 'Personnel',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='movement',
            name='author',
            field=models.ForeignKey(to='inventory.Person'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=250)),
                ('npa', models.CharField(max_length=5)),
                ('locality', models.CharField(max_length=50)),
                ('country', models.CharField(default='Suisse', max_length=50)),
                ('phone', models.CharField(default='', max_length=20, blank=True)),
                ('fax', models.CharField(default='', max_length=20, blank=True)),
                ('email', models.CharField(default='', max_length=100, blank=True)),
                ('web', models.CharField(default='', max_length=100, blank=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Fournisseur',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='provider',
            field=models.ForeignKey(verbose_name='Fournisseur', to='inventory.Provider'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Quantity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.DecimalField(help_text="Prix \xe0 l'unit\xe9", max_digits=8, decimal_places=2)),
                ('material', models.ForeignKey(to='inventory.Material')),
            ],
            options={
                'verbose_name': 'Quantit\xe9',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('number',),
                'verbose_name': 'Salle',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Armoire',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='quantity',
            name='storage',
            field=models.ForeignKey(to='inventory.Storage'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='quantity',
            unique_together=set([('material', 'storage')]),
        ),
        migrations.AddField(
            model_name='movement',
            name='storage',
            field=models.ForeignKey(to='inventory.Storage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='storage',
            name='materials',
            field=models.ManyToManyField(to='inventory.Material', through='inventory.Quantity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='storage',
            name='room',
            field=models.ForeignKey(to='inventory.Room'),
            preserve_default=True,
        ),
    ]
