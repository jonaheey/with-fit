# Generated by Django 3.2.10 on 2021-12-23 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fitness',
            fields=[
                ('fitness_index', models.BigAutoField(primary_key=True, serialize=False)),
                ('fitness_name', models.CharField(max_length=100)),
                ('guide', models.TextField(default='')),
                ('video', models.CharField(max_length=1000, null=True)),
            ],
            options={
                'db_table': 'fitness',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_index', models.BigAutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=100)),
                ('item_filename', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'item',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('monster_index', models.BigAutoField(primary_key=True, serialize=False)),
                ('monster_name', models.CharField(max_length=100)),
                ('monster_health', models.IntegerField()),
            ],
            options={
                'db_table': 'monster',
                'managed': True,
            },
        ),
    ]
