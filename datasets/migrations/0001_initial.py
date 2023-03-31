# Generated by Django 4.1.7 on 2023-03-31 16:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset_name', models.CharField(max_length=255)),
                ('about_info', models.TextField(blank=True)),
                ('last_updated', models.CharField(blank=True, max_length=255)),
                ('dataset_file_format', models.CharField(blank=True, max_length=255)),
                ('dataset_status', models.CharField(blank=True, max_length=255)),
                ('sponsor_name', models.CharField(blank=True, max_length=255)),
                ('access_type', models.CharField(blank=True, max_length=255)),
                ('dataset_link', models.CharField(blank=True, max_length=255)),
                ('dataset_website_link', models.CharField(blank=True, max_length=255)),
                ('dataset_citation', models.TextField(blank=True)),
                ('dataset_collection_method', models.TextField(blank=True)),
                ('last_scraped', models.CharField(blank=True, max_length=255)),
                ('other_info', models.TextField(blank=True)),
                ('collection', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='datasets', to='datasets.collection')),
            ],
        ),
        migrations.CreateModel(
            name='ModificationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('changes', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=255)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modification_requests', to='datasets.dataset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modification_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
