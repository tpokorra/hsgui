from django import forms

class DomainsAddForm(forms.Form):
    domain = forms.CharField(label='Domain', max_length=100)
    owner = forms.CharField(label='Owner', max_length=100)
