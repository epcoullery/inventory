# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *


class StorageInline(admin.TabularInline):
    model = Storage

class RoomAdmin(admin.ModelAdmin):
    inlines = [StorageInline]


admin.site.register(Material)
admin.site.register(Room)
admin.site.register(Person)
admin.site.register(Movement)
admin.site.register(Provider)
admin.site.register(Order)
