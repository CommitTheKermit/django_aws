# Generated by Django 4.2.1 on 2023-06-06 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visithistory',
            name='cafe',
        ),
        migrations.RemoveField(
            model_name='visithistory',
            name='user',
        ),
        migrations.DeleteModel(
            name='CafeRating',
        ),
        migrations.DeleteModel(
            name='VisitHistory',
        ),
    ]
