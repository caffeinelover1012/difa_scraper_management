from django import forms
from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm
from datasets.models import DataifaUser,VerificationQuestion, UserProfile
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.functional import lazy
from django.utils.translation import gettext as _
from datasets.models import Dataset, Collection

# from hcaptcha_field import hCaptchaField

from .models import DataifaUser

class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = DataifaUser
        fields = ['first_name', 'last_name']
        
class DifaSignInForm(LoginForm):
    # captcha = hCaptchaField()
    pass

class DifaSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=False)
    verification_question_1 = forms.ChoiceField(choices=VerificationQuestion.VERIFICATION_QUESTIONS, label='Verification Question 1')
    verification_answer_1 = forms.CharField(max_length=255, label='Answer 1', required=True)
    verification_question_2 = forms.ChoiceField(choices=VerificationQuestion.VERIFICATION_QUESTIONS, label='Verification Question 2')
    verification_answer_2 = forms.CharField(max_length=255, label='Answer 2', required=True)
    verification_question_3 = forms.ChoiceField(choices=VerificationQuestion.VERIFICATION_QUESTIONS, label='Verification Question 3')
    verification_answer_3 = forms.CharField(max_length=255, label='Answer 3', required=True)

    tc = forms.BooleanField(
        required=True,
        label = lazy(lambda: mark_safe(_(
            'I accept <a href="%s" target="_blank">Terms and Conditions</a>' % reverse('tnc')
        ))),
        label_suffix=''
    )
    # captcha = hCaptchaField()

    field_order = ['email', 'first_name', 'last_name', 'password1', 'password2', 'verification_question_1', 'verification_answer_1', 'verification_question_2', 'verification_answer_2', 'verification_question_3', 'verification_answer_3', 'tc', 'captcha']

    def clean_email(self):
        email = self.cleaned_data['email']
        if DataifaUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists. Please login instead.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        questions = [
            cleaned_data.get("verification_question_1"),
            cleaned_data.get("verification_question_2"),
            cleaned_data.get("verification_question_3")
        ]

        if len(set(questions)) != len(questions):
            raise forms.ValidationError("Please select different verification questions.")

        return cleaned_data
    
    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        for i in range(1, 4):
            question_field = f'verification_question_{i}'
            answer_field = f'verification_answer_{i}'
            VerificationQuestion.objects.create(
                user=user,
                question=self.cleaned_data[question_field],
                answer=self.cleaned_data[answer_field]
            )
        user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['institution_employer_name', 'institution_personal_website', 
                  'occupation_category', 'occupation_title', 'field_of_research', 'research_areas', 
                  'general_research_statement', 'how_did_you_learn']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        required_fields = ['institution_employer_name', 'occupation_category', 
                           'field_of_research', 'general_research_statement']
        for field_name in required_fields:
            self.fields[field_name].required = True


class DifaResetPasswordForm(ResetPasswordForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        UserModel = get_user_model()
        if not UserModel.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("No user registered with this email address.")
        return email

    def save(self, request, **kwargs):
        # Fetch the users before calling the super save method
        UserModel = get_user_model()
        self.users = UserModel.objects.filter(email__iexact=self.cleaned_data["email"], is_active=True)
        # Call the super method with the request and kwargs
        super().save(request, **kwargs)

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