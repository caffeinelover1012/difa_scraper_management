# Generated by Django 4.1.7 on 2023-04-28 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0005_alter_person_difa_workshop_presentation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='more_information',
            field=models.URLField(blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='presentation_slides',
            field=models.FileField(blank=True, null=True, upload_to='persons/presentation_slides/'),
        ),
    ]
