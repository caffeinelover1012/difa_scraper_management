# Generated by Django 4.1.7 on 2023-06-17 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0008_person_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='dataset_file_format',
            field=models.CharField(blank=True, max_length=1024),
        ),
    ]
