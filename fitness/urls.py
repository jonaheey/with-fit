from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    path('', views.index, name='index'), # 메인
    # path('select/', views.select, name='select'), # 운동, 인원 수 선택
    path('exercise/', views.exercise, name="exercise"),
    path('player/', views.player, name='player'),
    path('play/', views.play, name='play'), # 플레이
]

# https://dev-yakuza.posstree.com/ko/django/view/