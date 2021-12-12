# -*- coding: UTF-8 -*-
import numpy as np
import cv2 as cv
from pathlib import Path
from model.Tracking.deep_sort import preprocessing
from model.Tracking.deep_sort.nn_matching import NearestNeighborDistanceMetric
from model.Tracking.deep_sort.detection import Detection
from model.Tracking import generate_dets as gdet
from model.Tracking.deep_sort.tracker import Tracker
from tensorflow.keras.models import load_model
from tensorflow.keras.backend import set_session
import tensorflow as tf
from model.Action.action_enum import Actions, Squat_Actions

# Use Deep-sort(Simple Online and Realtime Tracking)
# 실시간 오브젝트 트래킹 (모델)
# https://github.com/nwojke/deep_sort
# To track multi-person for multi-person actions recognition
file_path = Path.cwd()
clip_length = 15
max_cosine_distance = 0.3
nn_budget = None
nms_max_overlap = 1.0
print(file_path)
# deep_sort
# MARS 데이터를 이용한 Person 분류 모델
model_filename = str(file_path/'model/Tracking/graph_model/mars-small128.pb')
encoder = gdet.create_box_encoder(model_filename, batch_size=1)
metric = NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
tracker = Tracker(metric)

sess = tf.Session()
graph = tf.get_default_graph()

# track_box
trk_clr = (0, 255, 0)



def load_action_premodel(model):
    set_session(sess)
    return load_model(model)

def framewise_recognize(pose, pretrained_model, player_list):
    frame, joints, bboxes, xcenter = pose[0], pose[1], pose[2], pose[3]
    joints_norm_per_frame = np.array(pose[-1])
    global sess
    global graph


    if bboxes:
        bboxes = np.array(bboxes)
        features = encoder(frame, bboxes)

        # score to 1.0 here).
        detections = [Detection(bbox, 1.0, feature) for bbox, feature in zip(bboxes, features)]

        boxes = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        indices = preprocessing.non_max_suppression(boxes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]

        # 트래커 실시간 업데이트
        tracker.predict()
        tracker.update(detections)
        
        
        # 바운딩 박스, 해당 ID를 포함한 결과
        trk_result = []
        for trk in tracker.tracks:
            if not trk.is_confirmed() or trk.time_since_update > 1:
                continue
            bbox = trk.to_tlwh()
            trk_result.append([bbox[0], bbox[1], bbox[2], bbox[3], trk.track_id])
            # track_ID 구별 표시
            trk_id = 'ID-' + str(trk.track_id)
            set_id = int(trk.track_id) - 1
            # 플레이어 설정 (track_id는 1부터 시작)
            if set_id + 1 <= len(player_list):
                player_list[set_id][0] = set_id

            cv.putText(frame, trk_id, (int(bbox[0]), int(bbox[1]-45)), cv.FONT_HERSHEY_SIMPLEX, 0.8, trk_clr, 3)
            
        for d in trk_result:
            xmin = int(d[0])
            ymin = int(d[1])
            xmax = int(d[2]) + xmin
            ymax = int(d[3]) + ymin
            id = int(d[4]) - 1

            try:
                tmp = np.array([abs(i - (xmax + xmin) / 2.) for i in xcenter])
                j = np.argmin(tmp)
            except:
                j = 0
            
            with graph.as_default():
                if joints_norm_per_frame.size > 0:
                    joints_norm_single_person = joints_norm_per_frame[j*36:(j+1)*36]
                    joints_norm_single_person = np.array(joints_norm_single_person).reshape(-1, 36)
                    set_session(sess)
                    pred = np.argmax(pretrained_model.predict(joints_norm_single_person))
                    if player_list[0][1] == 0:
                        init_label = Actions(pred).name
                    if player_list[0][1] == 1:
                        init_label = Squat_Actions(pred).name
                    
                    if id <= len(player_list):

                        exercise_Count(id, init_label, player_list)

                        count_text = str(player_list[id][3])
                        cv.putText(frame, count_text, (xmin + 80, ymin - 85), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
                    

                    # 텍스트 출력
                    cv.putText(frame, init_label, (xmin + 80, ymin - 45), cv.FONT_HERSHEY_SIMPLEX, 1, trk_clr, 3)
                    
            # track_box
            cv.rectangle(frame, (xmin - 10, ymin - 30), (xmax + 10, ymax), trk_clr, 2)

    return frame


# 운동에 따른 알고리즘 분류 함수
def exercise_Count(id, init_label, player_list):
    player_list[id][2] = init_label
    
    print(player_list[id])
    # 스탠딩 니업 일 경우
    if player_list[id][1] == 0:
        standing_Kneeup(id, player_list)


# 스탠딩 니업 카운트 함수
def standing_Kneeup(id, player_list):
    if player_list[id][2] == 'stand'      and player_list[id][4] == False:
        player_list[id][4] = True
    elif player_list[id][2] == 'right_up' and player_list[id][4] == True and player_list[id][5] == False:
        player_list[id][5] = True
    elif player_list[id][2] == 'stand'    and player_list[id][5] == True and player_list[id][6] == False:
        player_list[id][6] = True
    elif player_list[id][2] == 'left_up'  and player_list[id][6] == True and player_list[id][7] == False:
        player_list[id][7] = True
    elif player_list[id][2] == 'stand'    and player_list[id][7] == True and player_list[id][8] == False:
        player_list[id][8] = True
    
    if player_list[id][8] == True:
        player_list[id][3] += 1
        player_list[id][4:9] = [False, False, False, False, False]
    