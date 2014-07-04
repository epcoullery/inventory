# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.utils.safestring import mark_safe


class MainAdminSite(AdminSite):
    index_template = 'admin/main.html'
    site_header = mark_safe("École Pierre-Coullery<br>Gestion du matériel")
    site_title = "Gestion de matériel"

admin_site = MainAdminSite()
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
