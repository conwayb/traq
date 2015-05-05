from django import forms
from django.forms import ModelForm
from .models import Requirement

class RequirementForm(ModelForm):

    class Meta:
        model = Requirement
        fields = ['title', 'description', 'due_date', 'milestone']
        widgets = {
                "due_date": forms.DateInput(attrs={'type':'date'})
        }
class RequirementApproveForm(ModelForm):
    class Meta:
        model = Requirement
        fields = ['approved',]


