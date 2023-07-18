# Generated by Django 4.2.3 on 2023-07-18 06:14

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tasklists', '0002_alter_task_screenshot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='screenshot',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='tasklists/screenshots/', verbose_name='screenshot'),
        ),
    ]
