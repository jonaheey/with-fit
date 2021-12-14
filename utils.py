# -*- coding: UTF-8 -*-
import cv2 as cv
import os
import sys
from pathlib import Path
from model.Pose.pose_visualizer import TfPoseVisualizer

file_path = Path.cwd()
out_file_path = Path(file_path / "test_out/")

# 웹캠 해상도 설정 변수
cam_width, cam_height = 1280, 720

# Input 모델 해상도 설정
# VGG trained in 656*368; 
# mobilenet_thin trained in 432*368 (from tf-pose-estimation)
input_width, input_height = 656, 368

# 웹캠 동작 코드 (옵션 - 동영상으로 동작시킬시엔 비디오로 동작)
def choose_run_mode(args):
    """
    video or webcam
    """
    global out_file_path
    if args.video:
        # Open the video file
        if not os.path.isfile(args.video):
            print("Input video file ", args.video, " doesn't exist")
            sys.exit(1)
        cap = cv.VideoCapture(args.video)
        out_file_path = str(out_file_path / (args.video[:-4] + '_tf_out.mp4'))
    else:
        # 웹캠 Input
        cap = cv.VideoCapture(0, cv.CAP_DSHOW)

        # 웹캠 해상도 설정
        cap.set(cv.CAP_PROP_FRAME_WIDTH, cam_width)
        cap.set(cv.CAP_PROP_FRAME_HEIGHT, cam_height)
        out_file_path = str(out_file_path / 'webcam_tf_out.mp4')
    return cap

# Input 모델 불러오기
def load_pretrain_model(model):
    dyn_graph_path = {
        'VGG_origin': str(file_path / "model/Pose/graph_models/VGG_origin/graph_opt.pb"),
        'mobilenet_thin': str(file_path / "model/Pose/graph_models/mobilenet_thin/graph_opt.pb")
    }
    graph_path = dyn_graph_path[model]
    if not os.path.isfile(graph_path):
        raise Exception('Graph file doesn\'t exist, path=%s' % graph_path)

    return TfPoseVisualizer(graph_path, target_size=(input_width, input_height))


def set_video_writer(cap, write_fps=15):
    return cv.VideoWriter(out_file_path,
                          cv.VideoWriter_fourcc(*'mp4v'),
                          write_fps,
                          (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)), round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))
