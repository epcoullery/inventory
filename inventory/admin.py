# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *


class StorageInline(admin.TabularInline):
    model = Storage

class RoomAdmin(admin.ModelAdmin):
    inlines = [StorageInline]

class QuantityInline(admin.TabularInline):
    model = Quantity
    extra = 0

class StorageAdmin(admin.ModelAdmin):
    inlines = [QuantityInline]

class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('code', 'description')
    ordering = ('description',)
    inlines = [QuantityInline]

admin.site.register(Material, MaterialAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Person)
admin.site.register(Movement)
admin.site.register(Provider)
admin.site.register(Order)
