# Generated by Django 4.2 on 2024-11-08 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WellnessAI', '0016_remove_contact_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='updatedata',
            name='address',
        ),
        migrations.RemoveField(
            model_name='updatedata',
            name='age',
        ),
        migrations.RemoveField(
            model_name='updatedata',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='updatedata',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='updatedata',
            name='name',
        ),
        migrations.RemoveField(
            model_name='updatedata',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='updatedata',
            name='weight',
        ),
        migrations.AlterField(
            model_name='contact',
            name='subject',
            field=models.CharField(max_length=255),
        ),
    ]
