# Generated by Django 4.2.1 on 2023-06-22 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetings',
            name='meeting_participants',
            field=models.CharField(blank=True, max_length=5000),
        ),
    ]
