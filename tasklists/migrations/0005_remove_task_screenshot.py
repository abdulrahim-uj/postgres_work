# Generated by Django 4.2.3 on 2023-07-18 06:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasklists', '0004_alter_task_screenshot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='screenshot',
        ),
    ]
