# Generated by Django 5.0.6 on 2024-06-10 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_approvedemployer_user_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approvedemployer',
            name='user_type',
        ),
    ]
