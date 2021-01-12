# Generated by Django 3.1.4 on 2021-01-04 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('f_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('gu', models.CharField(max_length=45)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('tel', models.CharField(blank=True, max_length=45, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=45, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'facility',
                'managed': False,
            },
        ),
    ]
