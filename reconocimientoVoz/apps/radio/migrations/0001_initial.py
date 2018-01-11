# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-09 16:33
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProgramasRadiales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, verbose_name='Nombre del programa de radio')),
                ('dias', multiselectfield.db.fields.MultiSelectField(choices=[('lun', 'Lunes'), ('mar', 'Martes'), ('mie', 'Miercoles'), ('jue', 'Jueves'), ('vie', 'Viernes'), ('sab', 'Sábado'), ('dom', 'Domingo')], max_length=40, verbose_name='Selecciona los días')),
                ('inicio', models.TimeField(null=True)),
                ('duracion', models.PositiveSmallIntegerField(default=False, verbose_name='Duración del programa(minutos)')),
            ],
            options={
                'verbose_name_plural': 'programas radiales',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Radio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('radio', models.CharField(max_length=50, verbose_name='Nombre de la Emisora')),
                ('web', models.URLField()),
            ],
            options={
                'verbose_name_plural': 'radios',
                'ordering': ['radio'],
            },
        ),
    ]
