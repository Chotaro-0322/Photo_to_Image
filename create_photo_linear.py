# -*- coding: utf-8 -*-
import cv2
import numpy as np

from matplotlib import pyplot as plt
import math
import glob
import argparse

# パノラマ変換
def panorama_ougi(img):
    """
    引数：
        img: OpenCV形式の画像
    """
    # 全方位画像は正方形であることを前提にしている
    _, h , _ = img.shape
    # h_hanは半径などを表す
    h_han = int(h / 2)
    width = h_han - 270
    pano_width = 1500

    # 投影後のグリッドの作成
    radius, ori_theta = np.mgrid[:width, :pano_width]
    # 投影する画像面の作成
    dst = np.zeros((width, pano_width, 3))

    # 投影前の対応点の座標を計算
    # (x, y)を中心に平行移動してから回転行列を掛け算
    # 射影する目標
    for r in range(0, width):
        for theta in range(0, pano_width):
            #print("r, theta is ", r, theta)
            x = (r + h_han*0.5) * np.cos(np.deg2rad(theta*(360/pano_width))) + h_han # 元の座標を計算.
            y = (r + h_han*0.5) * np.sin(np.deg2rad(theta*(360/pano_width))) + h_han
            #print(x, y)
            dx = x - int(x) #微小値の計算
            dy = y - int(y)

            x = int(x) # 小数点切り捨てを行い, x = x0, y = y0を設定.
            y = int(y)

            dst[r ,theta, :] = (1 - dx)*(1 - dy) * img[y, x, :] + dx*(1 - dy)*img[y, x+1, :] + \
                                        (1 - dx)*dy*img[y+1, x, :] + dx*dy*img[y, x, :]
    # 出力サイズの調整
    dst = cv2.resize(dst, dsize=(pano_width, width))
    dst = dst.astype(np.int)
    # torch.Tensorに変更するために、float32に変更
    # plt.imshow()などで表示する場合はnp.uint8に変更する
    return dst.astype(np.float32)

# 3秒ごとにTrueを出力するプログラム
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
parser = argparse.ArgumentParser()
parser.add_argument("in_path", help="Please set a path of fileto video")
parser.add_argument("out_path", help="Please set a path of folder to save")
parser.add_argument("sec", help="Please set second of dividing")

args = parser.parse_args()

sec = float(args.sec)

cap = cv2.VideoCapture(args.in_path)

ret, frame = cap.read()

ret, frame = cap.read()
max_sec = 0

index_of_photo = 1

while(ret == True):
    ret, frame = cap.read()
    bool_of_sec, max_sec = sec_count(cap.get(cv2.CAP_PROP_POS_MSEC)/1000, max_sec, sec)
    if bool_of_sec == True:
        img = panorama_ougi(frame)
        img = img.astype(np.uint8)
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(args.out_path + '/{}.jpg'.format(str(index_of_photo).zfill(4)), img)
        print(args.out_path + '/{}.jpg was saved.'.format(str(index_of_photo).zfill(4)))
        index_of_photo += 1
print('Finished!!')


