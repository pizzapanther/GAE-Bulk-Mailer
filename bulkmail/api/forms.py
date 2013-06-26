from django import forms

class ApiKeyForm (forms.Form):
  name = forms.CharField(max_length=140)
  