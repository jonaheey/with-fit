from django.shortcuts import render, redirect
from django.http.response import HttpResponseRedirect



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
  return render(request, 'fitness/result.html')


# 운동, 인원수 선택
# def select(request):
#     # 운동 선택 후
#     if request.method == 'POST':
#         # 선택된 운동 값
#         exercise_name = request.POST.get('selected_e')

#         if exercise_name == '푸시업':
#             exercise_img = 'push_up'
#         elif exercise_name == '사이드 런지':
#             exercise_img = 'side_lunge'
#         elif exercise_name == '스탠딩 니 업':
#             exercise_img = 'standing_knee_up'
#         else:
#             exercise_img = 'step_forward_lunge'

#         # 인원 수 선택 화면으로 넘어감
#         return render(
#             request,
#             'people.html',
#             {'exercise_name' : exercise_name,
#              'exercise_img' : exercise_img}
#         )
#     # 운동 선택 화면
#     return render(
#         request,
#         'exercise.html'
#     )
