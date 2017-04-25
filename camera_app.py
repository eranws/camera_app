#!/usr/bin/env python

'''
Camera App

This boilerplate code sample opens camera or video and shows a frame

Usage:
  camera_app.py [--pause] [<video source>]

  --pause  -  Start with playback paused at the first video frame.
  
Keys:
  Esc      - exit app
  SPACE    - pause video

ripped off from mosse.py, MOSSE tracking sample, OpenCV
'''

import numpy as np
import cv2
import video

class App:
    def __init__(self, video_src, paused = False):
        self.cap = video.create_capture(video_src)
        _, self.frame = self.cap.read()
        cv2.imshow('frame', self.frame)
        self.paused = paused
        self.state = 0

    def run(self):
        while True:
            if not self.paused:
                ret, self.frame = self.cap.read()
                if not ret:
                    break
                frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            vis = frame_gray.copy()
            h, w = vis.shape[:2]

            A = 5

            m = w/3/A
            n = h/2/A

            w1 = w/2
            h1 = h/2
            
            for i in range(A):
                for j in range(A):
                # vis[h0:h1,w1+(i-A/2)*m:w1+(i+1-A/2)*m] = cv2.mean(vis[h0:h1,w1+(i-A/2)*m:w1+(i+1-A/2)*m])[0]
                    vis[h1+(j-A/2)*n:h1+(j+1-A/2)*n,w1+(i-A/2)*m:w1+(i+1-A/2)*m] = cv2.mean(vis[h1+(j-A/2)*n:h1+(j+1-A/2)*n,w1+(i-A/2)*m:w1+(i+1-A/2)*m])[0]

            if self.state == 0:
                vis[:, 0:w1-(A/2)*m] = 0 
                vis[:, w1+(A/2+1)*m:] = 0 
            if self.state == 1:
                vis[:, 0:w1-(A/2)*m] = 0 
                vis[:, w1+(A/2+1)*m:] = 255 
            if self.state == 2:
                vis[:, 0:w1-(A/2)*m] = 255 
                vis[:, w1+(A/2+1)*m:] = 0 
            if self.state == 3:
                vis[:, 0:w1-(A/2)*m] = 255 
                vis[:, w1+(A/2+1)*m:] = 255 



            cv2.imshow('frame', vis)
            ch = cv2.waitKey(10)
            if ch == 27:
                break
            if ch == ord(' '):
                self.paused = not self.paused

            if ch == ord('s'):
                fn = 'shot.bmp' 
                cv2.imwrite(fn, vis)
                print fn, 'saved'

            if ch == ord('n'):
                # self.state += 1
                # self.state %= 4
                self.state %= 2
                self.state += 1


if __name__ == '__main__':
    print __doc__
    import sys, getopt
    opts, args = getopt.getopt(sys.argv[1:], '', ['pause'])
    opts = dict(opts)
    try: video_src = args[0]
    except: video_src = '1'

    App(video_src, paused = '--pause' in opts).run()
