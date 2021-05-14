import cv2
import numpy as np
import os

import math
import glob


# 1秒ごとにTrueを出力
def sec_count(cap_sec, max_sec, get_sec = 1):
    cap_sec = math.floor(cap_sec)
    if cap_sec != max_sec:
        max_sec += 1
        if max_sec%get_sec == 0:
            return True, max_sec
        else:
            return False, max_sec
    else:
        return False, max_sec

# ------------------------------------------------main-------------------------------------------------------------

def video_to_img(video_name, save_file, create_list=True):
    """
    cv2.VideoCaptureを使用するには, ffmpegをインストール
    pip install ffmpeg-python

    Example:
    video_name = ./20.10.12_videos/125_0005.MP4
    save_file = ./21.10.12_videos/
    """

    cap = cv2.VideoCapture(video_name)
    print("video ", cap.isOpened())
    ret, frame = cap.read()
    max_sec = 0
    index_of_photo = 1

    if create_list == True:
        img_list = []

    while(ret == True):
        ret, frame = cap.read()
        bool_of_fivesec, max_sec = sec_count(cap.get(cv2.CAP_PROP_POS_MSEC)/1000, max_sec)
        if bool_of_fivesec == True:
            img = frame.astype(np.uint8)
            if create_list == True:
                img_list.append(img)
                print("list have ", len(img_list))
            else:
                cv2.imwrite(save_file + '/omni_photo_{}.jpg'.format(str(index_of_photo).zfill(4)), img)
                print(save_file, '/omni_photo_{}.jpg was saved.'.format(str(index_of_photo).zfill(4)))
            index_of_photo += 1

    if create_list == True:
        print("img list is ", np.shape(img_list))
    print('Finished!!')




print(os.getcwd())
video_name = "./21.02.04_photo/green.mp4"
save_file = "./21.02.04_photo/photo/"
video_to_img(video_name, save_file, create_list=True)
