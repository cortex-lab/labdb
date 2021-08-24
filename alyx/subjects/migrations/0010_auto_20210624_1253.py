# Generated by Django 3.2.4 on 2021-06-24 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0009_auto_20201103_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allele',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='breedingpair',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='genotypetest',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='line',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='litter',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='sequence',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='source',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='species',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='strain',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='subjectrequest',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='zygosity',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
        migrations.AlterField(
            model_name='zygosityrule',
            name='json',
            field=models.JSONField(blank=True, help_text='Structured data, formatted in a user-defined way', null=True),
        ),
    ]
