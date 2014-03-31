# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin, messages
from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, CreateView

from .forms import MovementForm
from .models import Material, Order, Quantity, Room, Storage, Movement, Person


def cond_redirect(request):
    if request.user.is_authenticated():
        return redirect('/')
    else:
        return admin.site.login(request)

def home(request):
    cur_orders = Order.objects.filter(receive_date__isnull=True)
    missing_mat = Material.objects.annotate(total_quant=Sum('quantity__quantity')
                                 ).filter(total_quant__lt=F('threshold')
                                 ).exclude(pk__in=cur_orders.values_list('pk', flat=True))
    context = {
        'missing_mat': missing_mat,
        'cur_orders': cur_orders,
        'rooms': Room.objects.all().prefetch_related('storage_set')
    }
    return admin.site.index(request, extra_context=context)


class StorageView(DetailView):
    model = Storage
    template_name = 'inventory/storage.html'

    def get_context_data(self, **kwargs):
        context = super(StorageView, self).get_context_data(**kwargs)
        context.update({
            'other_storages': self.object.room.storage_set.exclude(pk=self.object.pk),
            'quant_items': self.object.quantity_set.select_related('material').extra(
                select={'lower_name':'lower(inventory_material.description)'}).order_by('lower_name'),
        })
        return context

class QuantityEditView(CreateView):
    model = Movement
    form_class = MovementForm

    def dispatch(self, request, *args, **kwargs):
        self.storage = get_object_or_404(Storage, pk=kwargs['pk'])
        return super(QuantityEditView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.material = get_object_or_404(Material, pk=request.GET.get('mat'))
        return super(QuantityEditView, self).get(request, *args, **kwargs)

    def get_initial(self):
        initial = super(QuantityEditView, self).get_initial()
        if self.request.method == 'GET':
            initial.update({
                'storage': self.storage,
                'op_plus': self.request.GET.get('op') == 'true',
                'material': self.material,
                'typ': 'use',
            })
            if initial['op_plus']:
                initial['typ'] = 'order'
            try:
                initial['author'] = Person.objects.get(user=self.request.user)
            except Person.DoesNotExist:
                pass
        return initial

    def get_context_data(self, **kwargs):
        context = super(QuantityEditView, self).get_context_data(**kwargs)
        context.update({
            'storage': self.storage,
        })
        return context

    def form_valid(self, form):
        self.object = form.save()
        if form.cleaned_data['op_plus']:
            messages.success(self.request, "Vous avez ajouté du matériel avec succès")
        else:
            messages.success(self.request, "Vous avez retiré du matériel avec succès")
        return HttpResponse(self.object.storage.get_absolute_url())
