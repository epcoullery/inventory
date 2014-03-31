# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib.admin import widgets

from .models import Movement


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
        self.fields['author'].label = "Qui ?"
        self.fields['when'].label = "Quand ?"
        self.fields['when'].widget = widgets.AdminSplitDateTime()
        self.fields['quantity'].label = "Combien ?"

    def clean(self):
        data = self.cleaned_data
        if not data['op_plus']:
            # Reverse quantity if this is a minus operation
            data['quantity'] *= -1
        return data
