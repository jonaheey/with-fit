from django.db import models

class Rank(models.Model):
  rank_score = models.IntegerField(null=True)
  option = models.CharField(max_length=1)
  rank_fitness_name = models.CharField(max_length=50)
  rank_user_name = models.CharField(max_length=50)
  fitness_index = models.ForeignKey('fitness.Fitness', on_delete=models.DO_NOTHING, db_column='fitness_index')
  user_index = models.ForeignKey('user.User', on_delete=models.CASCADE, db_column='user_index')

  class Meta:
    managed = True
    db_table = 'rank'
