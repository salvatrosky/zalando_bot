# Generated by Django 3.2.25 on 2024-05-19 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('EN', 'English'), ('IT', 'Italiano'), ('ES', 'Español')], default='IT', max_length=2),
        ),
    ]
