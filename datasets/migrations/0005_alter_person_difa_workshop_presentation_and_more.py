# Generated by Django 4.1.7 on 2023-04-28 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0004_person_show'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='difa_workshop_presentation',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='presentation_slides',
            field=models.FileField(null=True, upload_to='persons/presentation_slides/'),
        ),
    ]