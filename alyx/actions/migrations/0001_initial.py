# Generated by Django 2.0.6 on 2018-07-13 13:49

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OtherAction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('narrative', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProcedureType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('name', models.CharField(help_text='Short procedure name', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Detailed description of the procedure')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('narrative', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('type', models.CharField(blank=True, help_text='User-defined session type (e.g. Base, Experiment)', max_length=255, null=True)),
                ('number', models.IntegerField(blank=True, help_text='Optional session number for this level', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Surgery',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('narrative', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('outcome_type', models.CharField(blank=True, choices=[('a', 'Acute'), ('r', 'Recovery')], max_length=1)),
            ],
            options={
                'verbose_name_plural': 'surgeries',
            },
        ),
        migrations.CreateModel(
            name='VirusInjection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('narrative', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('virus_batch', models.CharField(blank=True, max_length=255, null=True)),
                ('injection_volume', models.FloatField(blank=True, help_text='Volume in nanoliters', null=True)),
                ('rate_of_injection', models.FloatField(blank=True, help_text='TODO: Nanoliters per second / per minute?', null=True)),
                ('injection_type', models.CharField(blank=True, choices=[('I', 'Iontophoresis'), ('P', 'Pressure')], default='I', help_text='Whether the injection was through iontophoresis or pressure', max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WaterAdministration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('water_administered', models.FloatField(help_text='Water administered, in millilitres', validators=[django.core.validators.MinValueValidator(limit_value=0)])),
                ('hydrogel', models.NullBooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WaterRestriction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('narrative', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Weighing',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('json', django.contrib.postgres.fields.jsonb.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True)),
                ('date_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('weight', models.FloatField(help_text='Weight in grams', validators=[django.core.validators.MinValueValidator(limit_value=0)])),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
