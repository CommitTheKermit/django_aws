# Generated by Django 3.2.18 on 2023-05-01 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='users_custom',
        ),
    ]