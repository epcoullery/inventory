# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django import forms
from django.contrib.admin import widgets
from django.core.urlresolvers import reverse

from .models import Material, Movement, Order, Person, Storage


class MovementForm(forms.ModelForm):
    # Tell if we are adding or substracting material
    op_plus = forms.BooleanField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Movement
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MovementForm, self).__init__(*args, **kwargs)
        if 'storage' in kwargs['initial']:
            self.fields['storage'].widget = forms.HiddenInput()
        if 'material' in kwargs['initial']:
            self.fields['material'].widget = forms.HiddenInput()
        else:
            self.fields['material'].queryset = Material.objects.order_by('description')
        self.fields['author'].label = "Qui ?"
        self.fields['when'].label = "Quand ?"
        self.fields['material'].label = "Quoi ?"
        self.fields['when'].widget = widgets.AdminSplitDateTime()
        self.fields['quantity'].label = "Combien ?"

    def clean(self):
        data = self.cleaned_data
        if not data['op_plus']:
            # Reverse quantity if this is a minus operation
            data['quantity'] *= -1
        return data


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            mat = self.instance.material
        else:
            mat = kwargs.get('initial', {}).get('material') or kwargs.get('data', {}).get('material')
        self.fields['quantity'].help_text = "Unité : %s" % mat.unit
        self.fields['order_date'].widget = widgets.AdminDateWidget()
        if self.instance.pk:
            self.action = reverse("material_receive")
            self.fields['receive_date'].widget = widgets.AdminDateWidget()
            self.fields['receive_date'].required = True
            self.fields['storage'] = forms.ModelChoiceField(
                label="Stockage initial", queryset=Storage.objects.all().order_by('room', 'code'))
        else:
            self.action = reverse("material_order")
            del self.fields['receive_date']
        if mat:
            self.fields['material'].widget = forms.HiddenInput()

    def save(self, request):
        super(OrderForm, self).save()
        # If receive_date is set, create a movement
        if self.instance.receive_date:
            pers, _ = Person.objects.get_or_create(user=request.user,
                defaults={'first_name': request.user.first_name, 'last_name': request.user.last_name})
            Movement.objects.create(
                author=Person.objects.get(user=request.user),
                typ='order',
                when=datetime.now(),
                material=self.instance.material,
                storage=Storage.objects.get(pk=request.POST.get('storage')),
                quantity=self.instance.quantity,
            )
