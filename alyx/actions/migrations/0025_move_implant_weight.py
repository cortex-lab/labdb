# Generated by Django 4.2.10 on 2024-03-15 13:53
"""
In 2024-03 the Subject.implant_weight field was removed and the Surgery.implant_weight field
was added.  This script 'saves' the non-zero implant weights to the Subject.JSON field and if
unambiguous, saves the implant weight to the relevent surgery.
"""
import logging
from pathlib import Path
from datetime import datetime, timezone

from django.db import migrations
from django.core import serializers

import alyx

logger = logging.getLogger(__name__)


def move_implant_weight(apps, schema_editor):
    Subject = apps.get_model('subjects', 'Subject')
    ProcedureType = apps.get_model('actions', 'ProcedureType')
    try:
        headplate_implant = ProcedureType.objects.get(name='Headplate implant')
    except ProcedureType.DoesNotExist:
        headplate_implant = None
    query = Subject.objects.filter(implant_weight__gt=0)
    now = datetime.now(timezone.utc).isoformat()
    n = 0
    for subject in query:
        # Add implant weight to JSON field for prosperity
        iw = subject.implant_weight
        json = subject.json or {}
        d = {'implant_weight': [{'value': iw, 'datetime': now}]}
        if 'history' in json:
            json['history'].update(d)
        else:
            json['history'] = d
        subject.json = json
        subject.save()
        # If possible, add implant weight to previous surgery
        surgeries = subject.actions_surgerys.filter(procedures__name__icontains='implant')
        if surgeries.count() == 0:
            # If no surgeries contain an implant procedure, attempt to find one surgery where
            # implant or headplate are mentioned in the narrative
            surgeries = subject.actions_surgerys.filter(narrative__iregex='.*(headplate|implant).*')
        # If there is an unambiguous result, set the surgery implant weight
        if surgeries.count() == 1:
            surgery = surgeries.first()
            surgery.implant_weight = iw
            # If headplate is mentioned in the narrative, add Headplate implant procedure
            # to the surgeries procedures list
            if headplate_implant and 'headplate' in surgery.narrative.lower():
                surgery.procedures.add(headplate_implant)
            surgery.save()
            n += 1

    logger.info(f'implant weights: {query.count():,g} subjects; {n:,g} surgeries updated')
    if query.count():
        filename = now[:19].replace(':', '-') + '_subject-implant-weight.json'
        filepath = Path(alyx.__file__).parents[2].joinpath('data', filename)
        with open(filepath, 'w') as fp:
            fp.write(serializers.serialize('json', query, fields=['implant_weight']))


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0024_surgery_implant_weight'),
    ]

    operations = [migrations.RunPython(move_implant_weight)]
