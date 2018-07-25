# -*- coding: UTF-8 -*- #
# Author: Zander_M
# Time: 七月, 22, 2018
# Title: Testing sonypy
from sonypy import Camera, Discoverer
import msvcrt
import requests
import matplotlib
import cv2
import matplotlib as plt
import numpy as np

a = Discoverer().discover()
while len(a) == 0:
    a = Discoverer().discover()
if ord(msvcrt.getch()) in [68, 100]:
    cam = a[0]
    cam.start_rec_mode()
    # rep = cam.start_liveview()
    rep = cam.start_liveview_with_size("M")
    frame = cam.stream_liveview(rep)
    a = 0
    for i in frame:
        if a <= 10:
            a += 1
        else:
            fm = cv2.imdecode(np.fromstring(i, np.uint8), True)
            cv2.imshow("frame", fm) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    cam.stop_liveview()

        
        # for i in frame:
        #     # print(type(i))
        #     p = plt.imread(i)
        #     plt.imshow('frame', p )
        #     plt.show()
        #     while not input():
        #         pass
        #     # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     #     break
        # stm.release()
        # cv2.destroyAllWindows()

        
        
        
