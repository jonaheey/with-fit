from django.shortcuts import render

from django.views.decorators import gzip
from django.http import StreamingHttpResponse

import cv2
import threading

from utils import load_pretrain_model
from model.Pose.pose_visualizer import TfPoseVisualizer
from model.Action.recognizer import load_action_premodel, framewise_recognize

estimator = load_pretrain_model('VGG_origin')
action_classifier = load_action_premodel('model/Action/stnading_knee_scene/framewise_standing_knee_scene2.5.h5')

# 메인
def index(request):
    return render(
        request,
        'index.html'
    )

# 운동, 인원수 선택
def select(request):
    # 운동 선택 후
    if request.method == 'POST':
        # 선택된 운동 값
        exercise_name = request.POST.get('selected_e')

        if exercise_name == '푸시업':
            exercise_img = 'push_up'
        elif exercise_name == '사이드 런지':
            exercise_img = 'side_lunge'
        elif exercise_name == '스탠딩 니 업':
            exercise_img = 'standing_knee_up'
        else:
            exercise_img = 'step_forward_lunge'
        print(exercise_img)
        
        # 인원 수 선택 화면으로 넘어감
        return render(
            request,
            'people.html',
            {'exercise_name' : exercise_name,
             'exercise_img' : exercise_img}
        )
    # 운동 선택 화면
    return render(
        request,
        'exercise.html'
    )

# 플레이
def play(request):
    # 선택된 운동
    exercise_name = request.POST.get('exercise')

    # 선택된 인원수
    player = request.POST.get('selected_p')

    # 팀 이름
    team_name = request.POST.get('team_name')

    print(exercise_name, player, team_name)

    # 플레이 화면
    return render(
        request,
        'play.html',
    )



# ! model 추가
def home(request):
    context = {}

    return render(request, "play.html", context)

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()

        self.player_list = []
        # 임시 변수
        self.player = 256
        self.exercise = 0

        for i in range(self.player):
            self.player_list.append([i, self.exercise, 'now_pose', 0, False, False, False, False, False])

        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        humans = estimator.inference(image)
        pose = TfPoseVisualizer.draw_pose_rgb(image, humans)
        image  = framewise_recognize(pose, action_classifier, self.player_list)
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read() 
            # humans = estimator.inference(self.frame) 
            # pose = TfPoseVisualizer.draw_pose_rgb(self.frame, humans)
            # self.frame  = framewise_recognize(pose, self.player_list)

cam = VideoCamera()

def gen(camera):
    while True:
        frame = camera.get_frame()
        
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def webcam(request):
    try:
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass