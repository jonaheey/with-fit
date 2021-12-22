from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect

from user.models import User
from rank.models import Rank
from fitness.models import Fitness


def index(request):
  return render(request, 'index.html')



def select(request):
  return render(request, 'fitness/select.html')



def player(request):
  return render(request, 'fitness/player.html')


 
def play(request):
  if request.method == 'POST':
    exercise = request.POST.get('exercise')
    selected_p = request.POST.get('selected_p')

    print(exercise)
    print(selected_p)

    # 플레이 화면
    return render(request, 'fitness/play.html')

  else:
    return HttpResponseRedirect('fitness:index')



def result(request):
  if request.method == 'POST':
    score = int(request.POST.get('score'))
    option = request.POST.get('option')
    fitness_name = request.POST.get('fitness_name')
    user_name = request.POST.get('user_name')
    fitness_index = int(request.POST.get('fitness_index'))
    user_index = int(request.POST.get('user_index'))
    user_index = request.POST.get('user_index')
    stage = int(request.POST.get('stage'))
    
    rank = Rank(rank_score=score,
                option=option,
                rank_fitness_name=fitness_name,
                rank_user_name=user_name,
                fitness_index=Fitness.objects.get(fitness_index=fitness_index),
                user_index=User.objects.get(user_index=user_index),
                stage=stage
                )
    rank.save()

    return render(request, 'fitness/result.html')

    # 플레이 화면
  # try:
  #   rank_score = request.GET.get('rank_score')
  #   option = request.GET.get('option')
  #   rank_fitness_name = request.GET.get('fitness_name')
  #   rank_user_name = request.GET.get('user_name')
  #   stage = request.GET.get('stage')
  #   fitness_index = request.GET.get('fitness_name')
  #   user_index = request.GET.get('user_index')
    

  #   rank = Rank(rank_score=rank_score, option=option, rank_fitness_name=rank_fitness_name,
  #                 rank_user_name=rank_user_name, stage=stage, fitness_index=fitness_index, user_index=user_index)
  #   rank.save()

  #   Rank.objects.get()


  #   # 플레이 화면
  #   return JsonResponse(result)

  # return render(request, 'fitness/result.html')