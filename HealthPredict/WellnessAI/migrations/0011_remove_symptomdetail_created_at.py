# Generated by Django 4.2 on 2024-11-07 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WellnessAI', '0010_symptomdetail_created_at_alter_userdetail_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='symptomdetail',
            name='created_at',
        ),
    ]