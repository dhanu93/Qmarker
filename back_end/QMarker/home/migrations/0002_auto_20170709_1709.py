# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-09 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarkingAlgo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qId', models.IntegerField()),
                ('mark', models.FloatField()),
                ('point', models.FloatField()),
                ('system', models.IntegerField()),
                ('teacher_avg', models.FloatField()),
                ('weight', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=1000)),
                ('answer', models.CharField(max_length=1000)),
                ('mark', models.FloatField()),
            ],
        ),
        migrations.DeleteModel(
            name='McqPaper',
        ),
        migrations.DeleteModel(
            name='McqQuestions',
        ),
    ]