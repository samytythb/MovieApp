# Generated by Django 4.2.7 on 2023-11-21 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailerLink',
            field=models.TextField(default=' ', max_length=100),
        ),
    ]