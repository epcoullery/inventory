# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from common.admin import admin_site
from .models import *


class StorageInline(admin.TabularInline):
    model = Storage

class RoomAdmin(admin.ModelAdmin):
    inlines = [StorageInline]

class QuantityInline(admin.TabularInline):
    model = Quantity
    can_delete = False
    readonly_fields = ('storage', 'quantity', 'price')
    extra = 0
    max_num = 0

class StorageAdmin(admin.ModelAdmin):
    inlines = [QuantityInline]

class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('code', 'description')
    ordering = ('description',)
    inlines = [QuantityInline]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('material', 'quantity', 'order_date', 'receive_date')

admin_site.register(Material, MaterialAdmin)
admin_site.register(Room, RoomAdmin)
admin_site.register(Storage, StorageAdmin)
admin_site.register(Person)
admin_site.register(Movement)
admin_site.register(Provider)
admin_site.register(Order, OrderAdmin)
