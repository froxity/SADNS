# Generated by Django 4.0 on 2021-12-31 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_profileconfig_block'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profileconfig',
            name='block',
        ),
    ]
