# Generated by Django 3.1.4 on 2021-01-04 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('m_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=30)),
                ('f_id', models.CharField(max_length=10)),
                ('state', models.CharField(default='정상', max_length=10)),
            ],
            options={
                'db_table': 'bookmark',
                'managed': False,
            },
        ),
    ]
