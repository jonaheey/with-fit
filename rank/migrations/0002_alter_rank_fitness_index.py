# Generated by Django 4.0 on 2021-12-22 17:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fitness', '0001_initial'),
        ('rank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rank',
            name='fitness_index',
            field=models.ForeignKey(db_column='fitness_index', on_delete=django.db.models.deletion.CASCADE, to='fitness.fitness'),
        ),
    ]
