from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

class Collection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


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
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, related_name='datasets')

    def __str__(self):
        return self.dataset_name


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='modification_requests')
    changes = models.TextField(blank=True)  # You can use a JSONField if you want to store changes as JSON
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f'Modification Request {self.id} - {self.dataset.dataset_name} - {self.user.username}'
