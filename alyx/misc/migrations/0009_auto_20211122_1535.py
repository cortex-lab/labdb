# Generated by Django 3.2.5 on 2021-11-22 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0008_auto_20210624_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='object_id',
            field=models.UUIDField(help_text='UUID, an object of content_type with this ID must already exist to attach a note.'),
        ),
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.TextField(blank=True, help_text='String, content of the note or description of the image.'),
        ),
    ]
