# Generated by Django 5.0.6 on 2024-06-10 06:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_remove_approvedemployer_user_typee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvedseeker',
            name='user_type',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]