from django import forms
from django.core import validators
from second_app.models import Users

class NewForms(forms.ModelForm):
    #Add custom validation here
    #first_name = charfield(validations = "")
    class Meta:
        model = Users
        fields = '__all__'
        
    