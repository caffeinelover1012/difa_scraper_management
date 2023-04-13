from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Dataset(models.Model):
    dataset_name = models.CharField(max_length=255)
    about_info = models.TextField(blank=True)
    last_updated = models.CharField(max_length=255, blank=True)
    dataset_file_format = models.CharField(max_length=255, blank=True)
    dataset_status = models.CharField(max_length=255, blank=True)
    sponsor_name = models.CharField(max_length=255, blank=True)
    access_type = models.CharField(max_length=255, blank=True)
    dataset_link = models.CharField(max_length=255, blank=True)
    dataset_website_link = models.CharField(max_length=255, blank=True)
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
        return f'Modification Request {self.id} - {self.dataset.dataset_name} - {self.user.username}'
