# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Domaine',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='material',
            name='domain',
            field=models.ForeignKey(to='inventory.Domain', null=True),
            preserve_default=True,
        ),
    ]
