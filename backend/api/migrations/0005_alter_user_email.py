# Generated by Django 4.2.7 on 2023-11-22 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_rating_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254, unique=True),
        ),
    ]