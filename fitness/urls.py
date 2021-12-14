from django.urls import path
from . import views

app_name = 'fitness'

urlpatterns = [
    path('', views.index, name='index'), # 메인
    path('select/', views.select, name='select'), # 운동, 인원 수 선택
    path('play/', views.play, name='play'), # 플레이
    # path('webcam', views.webcam, name="webcam"), # 플레이 화면
]

# https://dev-yakuza.posstree.com/ko/django/view/