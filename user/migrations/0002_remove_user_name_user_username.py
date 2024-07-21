# Generated by Django 4.2.13 on 2024-07-18 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, error_messages={'unique': 'This email has been used already'}, max_length=150, unique=True, verbose_name='Username'),
        ),
    ]