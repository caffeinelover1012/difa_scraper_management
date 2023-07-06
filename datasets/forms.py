from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ModificationRequest, Dataset, Collection
from django.utils import timezone
from django.db import models

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64)
    password = forms.CharField(label='Password', max_length=64, widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    institution_employer_name = forms.CharField(max_length=100)
    institution_personal_website = forms.URLField(required=False)
    occupation_category = forms.CharField(max_length=100)
    occupation_title = forms.CharField(max_length=100)
    field_of_research = forms.CharField(max_length=100)
    research_areas = forms.CharField(max_length=255)
    general_research_statement = forms.CharField(max_length=255)
    how_did_you_learn = forms.CharField(max_length=255)
    class Meta:
        model = get_user_model()
        # print(model)
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name',
                  'institution_employer_name', 'institution_personal_website', 'occupation_category',
                  'occupation_title', 'field_of_research', 'research_areas', 'general_research_statement',
                  'how_did_you_learn')
#ListJS

class DatasetModificationRequestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        dataset = kwargs.pop('dataset', None)
        super(DatasetModificationRequestForm, self).__init__(*args, **kwargs)
        
        for field in Dataset._meta.get_fields():
            if field.name != 'last_scraped' and field.name != 'id' and field.name != 'collection'and hasattr(field, 'verbose_name'):
                self.fields[field.name] = forms.CharField(
                    label=field.verbose_name.capitalize().replace('_', ' '),
                    initial=getattr(dataset, field.name, ''),
                    widget=forms.Textarea(attrs={'rows': 1}) if field.name == 'other_info' else forms.TextInput()
                )

class CollectionForm(forms.ModelForm):
    datasets = forms.ModelMultipleChoiceField(
        queryset=Dataset.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )


    class Meta:
        model = Collection
        fields = ['name', 'description', 'datasets']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }