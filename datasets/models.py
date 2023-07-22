from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=30,blank=True)
    last_name = models.CharField(max_length=30,blank=True)
    institution_employer_name = models.CharField(max_length=100,blank=True)
    institution_personal_website = models.URLField(blank=True, null=True)
    occupation_category = models.CharField(max_length=100,blank=True)
    occupation_title = models.CharField(max_length=100,blank=True)
    field_of_research = models.CharField(max_length=100,blank=True)
    research_areas = models.CharField(max_length=255,blank=True)
    general_research_statement = models.CharField(max_length=255,blank=True)
    how_did_you_learn = models.CharField(max_length=255,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name

class Dataset(models.Model):
    dataset_name = models.CharField(max_length=700)
    about_info = models.TextField(blank=True)
    last_updated = models.CharField(max_length=255, blank=True)
    dataset_file_format = models.CharField(max_length=1024, blank=True)
    dataset_status = models.CharField(max_length=255, blank=True)
    sponsor_name = models.CharField(max_length=700, blank=True)
    access_type = models.CharField(max_length=255, blank=True)
    dataset_link = models.CharField(max_length=700, blank=True)
    dataset_website_link = models.CharField(max_length=700, blank=True)
    dataset_citation = models.TextField(blank=True)
    dataset_collection_method = models.TextField(blank=True)
    last_scraped = models.CharField(max_length=255, blank=True)
    other_info = models.TextField(blank=True)

    def __str__(self):
        return self.dataset_name


class Collection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(get_user_model(), null=True,on_delete=models.SET_NULL)
    datasets = models.ManyToManyField(Dataset, related_name='related_collections', related_query_name='collection')

    def __str__(self):
        return self.name


class ModificationRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]


    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='modification_requests')
    user = models.ForeignKey(get_user_model(),null=True, on_delete=models.SET_NULL, related_name='modification_requests')
    changes = models.TextField(blank=True)  # You can use a JSONField if you want to store changes as JSON
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=PENDING)
    approver = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.SET_NULL, related_name='approver_mod_requests')

    def __str__(self):
        return f'Modification Request {self.id} - {self.dataset.dataset_name} - {self.user.email}'


class Person(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='persons/images/')
    description = models.TextField()
    difa_workshop_presentation = models.URLField(null=True, blank=True)
    presentation_slides = models.FileField(upload_to='persons/presentation_slides/',blank=True, null=True)  # Add this line
    more_information = models.URLField(blank=True)
    TEAM_CHOICES = [
        ('leadership', 'Leadership Team'),
        ('research', 'Research Team'),
        ('guest', 'Guest'),
    ]
    team = models.CharField(max_length=20, choices=TEAM_CHOICES, default='guest')
    show = models.BooleanField(default=True)

    def __str__(self):
        return self.name
