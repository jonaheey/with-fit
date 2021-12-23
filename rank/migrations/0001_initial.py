# Generated by Django 4.0 on 2021-12-22 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fitness', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('rank_index', models.BigAutoField(primary_key=True, serialize=False)),
                ('rank_score', models.IntegerField(null=True)),
                ('option', models.CharField(max_length=1)),
                ('rank_fitness_name', models.CharField(max_length=50)),
                ('rank_user_name', models.CharField(max_length=50)),
                ('stage', models.IntegerField(null=True)),
                ('fitness_index', models.ForeignKey(db_column='fitness_index', on_delete=django.db.models.deletion.DO_NOTHING, to='fitness.fitness')),
                ('user_index', models.ForeignKey(db_column='user_index', on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'rank',
                'managed': True,
            },
        ),
    ]
