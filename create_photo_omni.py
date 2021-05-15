# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

import math
import glob
import argparse


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

def video_to_img(video_name, save_file, sec, create_list=True):
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
        bool_of_sec, max_sec = sec_count(cap.get(cv2.CAP_PROP_POS_MSEC)/1000, max_sec, sec)
        if bool_of_sec == True:
            img = frame.astype(np.uint8)
            if create_list == True:
                img_list.append(img)
                print("list have ", len(img_list))
                cv2.imwrite(save_file + '/omni_photo_{}.jpg'.format(str(index_of_photo).zfill(4)), img)
                print(save_file, '/omni_photo_{}.jpg was saved.'.format(str(index_of_photo).zfill(4)))
            index_of_photo += 1

    if create_list == True:
        print("img list is ", np.shape(img_list))
    print('Finished!!')


parser = argparse.ArgumentParser()
parser.add_argument("in_path", help="Please set a path of fileto video")
parser.add_argument("out_path", help="Please set a path of folder to save")
parser.add_argument("sec", help="Please set second of dividing")

args = parser.parse_args()

print(os.getcwd())
video_name = args.in_path
save_file = args.out_path
sec = float(args.sec)
video_to_img(video_name, save_file, sec, create_list=True)
