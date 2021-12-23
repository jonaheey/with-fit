from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect, JsonResponse

from django.core import serializers

from user.models import User
from rank.models import Rank
from fitness.models import Fitness

import json

def index(request):
  return render(request, 'index.html')

def get_rank(request):
  num = 4
  rank = Rank.objects.order_by('-rank_score')[:num]

  rank_data = serializers.serialize('json', rank, fields={'rank_user_name', 'rank_score', 'rank_fitness_name', 'option'})
  rank_data = json.loads(rank_data)
  rank_data = [{**item['fields'], **{'pk': item['pk']}} for item in rank_data]
  context = {
    'num': num,
    'rank_data': rank_data
  }

  return JsonResponse(context)


def select(request):
  return render(request, 'fitness/select.html')


def player(request):
  return render(request, 'fitness/player.html')


def play(request):
  if request.method == 'POST':
    # 선택된 운동
    exercise_name = request.POST.get('exercise')

    # 선택된 인원수
    player = request.POST.get('selected_p')

    fitness = Fitness.objects.get(fitness_name=exercise_name)
    fitness_index = fitness.fitness_index

    context = {
      'exercise_name': exercise_name,
      'player': player,
      'fitness_index': fitness_index
    }
    
    if player == '1':
      return render(request, 'fitness/play.html', context)
    elif player == '2':
      return render(request, 'fitness/play2p.html', context)

  else:
    return HttpResponseRedirect('fitness:index')


def play2p(request):
  if request.method == 'POST':
    # 선택된 운동
    exercise_name = request.POST.get('exercise')
    

def result(request):
  if request.method == 'POST':
    score = request.POST.get('score')
    option = request.POST.get('option')
    fitness_name = request.POST.get('fitness_name')
    user_name = request.POST.get('user_name')
    fitness_index = int(request.POST.get('fitness_index'))
    user_index = int(request.POST.get('user_index'))
    # stage = request.POST.get('stage')
    stage = 3

    try:
      rank = Rank.objects.get(user_index=user_index, fitness_index=fitness_index)
      if score > rank.rank_score:
        rank.rank_score = score
        rank.save()
    except Exception as e:
      rank = Rank(rank_score=score,
          option=option,
          rank_fitness_name=fitness_name,
          rank_user_name=user_name,
          fitness_index=Fitness.objects.get(fitness_index=fitness_index),
          user_index=User.objects.get(user_index=user_index),
          stage=stage
      )
      rank.save()

    index_data = {
      'user_index': user_index
    }

    return render(request, 'fitness/result.html', index_data)
    
  return HttpResponseRedirect('fitness:index')

def get_result(request):
  result_rank = Rank.objects.all().order_by('-rank_score')

  result_data = serializers.serialize('json', result_rank, fields={'rank_user_name', 'rank_score', 'rank_fitness_name', 'stage', 'option'})
  result_data = json.loads(result_data)
  result_data = [{**item['fields'], **{'pk': item['pk']}} for item in result_data]

  context = {
    'result_data': result_data
  }

  return JsonResponse(context)