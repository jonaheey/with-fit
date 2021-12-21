from django.db import models

class Fitness(models.Model):
  fitness_index = models.IntegerField(primary_key=True)
  fitness_name = models.CharField(max_length=100)
  guide = models.TextField(default="")
  video = models.CharField(max_length=1000, null=True)

  class Meta:
    managed = True
    db_table = 'fitness'


class Enemy(models.Model):
  enemy_index = models.BigAutoField(primary_key=True)
  enemy_name = models.CharField(max_length=100)
  health = models.IntegerField()
  enemy_filename = models.CharField(max_length=300)

  class Meta:
    managed = True
    db_table = 'enemy'


class Item(models.Model):
  item_index = models.BigAutoField(primary_key=True)
  item_name = models.CharField(max_length=100)
  item_filename = models.CharField(max_length=1000)

  class Meta:
    managed = True
    db_table = 'item'