# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.admin import widgets

from .models import Material, Movement, Order


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
        self.fields['order_date'].widget = widgets.AdminDateWidget()
        if self.instance.pk:
            self.fields['receive_date'].widget = widgets.AdminDateWidget()
        else:
            del self.fields['receive_date']
        if 'material' in kwargs['initial'] or 'material' in kwargs['data']:
            self.fields['material'].widget = forms.HiddenInput()
