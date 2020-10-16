from django import forms
from .models import DataStore

class DataForm(forms.ModelForm):
	class Meta:
		model = DataStore
		exclude = ('slug',)
