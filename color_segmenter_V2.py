#!/usr/bin/env python
from os import path
import cv2
import numpy as np
import argparse
from functools import partial
from colorama import Fore, Style
import json
from functions import update_range_vals, apply_mask

def main():
    file_Existence = path.exists('limits,json')

    if file_Existence:
        with open('limits.json', 'r') as openfile:
            json_file = json.load(openfile)
            tck_ranges = json_file['limits']
    else:
        tck_ranges = {'B': {'max': 255, 'min': 0}, 'G': {'max': 255, 'min': 0}, 'R': {'max': 255, 'min': 0}}
    
    video_capture = cv2.VideoCapture(0)
    result, video_frame = video_capture.read()
    if result is False:
        print('Your camera isn\'t working, press any key to exit')
        cv2.waitKey(0)
        exit(0) 

    scale = 0.6
    window_width = int(video_frame.shape[1] * scale)
    window_height = int(video_frame.shape[0])

    window_name = 'Color Segmenter'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, window_width, window_height)

    cv2.createTrackbar('R min', window_name, tck_ranges['R']['min'], 255, partial(update_range_vals, dict_ranges = tck_ranges, color = 'R', bound = 'min'))
    cv2.createTrackbar('R max', window_name, tck_ranges['R']['max'], 255, partial(update_range_vals, dict_ranges = tck_ranges, color = 'R', bound = 'max'))
    cv2.createTrackbar('G min', window_name, tck_ranges['G']['min'], 255, partial(update_range_vals, dict_ranges = tck_ranges, color = 'G', bound = 'min'))
    cv2.createTrackbar('G max', window_name, tck_ranges['G']['max'], 255, partial(update_range_vals, dict_ranges = tck_ranges, color = 'G', bound = 'max'))
    cv2.createTrackbar('B min', window_name, tck_ranges['B']['min'], 255, partial(update_range_vals, dict_ranges = tck_ranges, color = 'B', bound = 'min'))
    cv2.createTrackbar('B max', window_name, tck_ranges['B']['max'], 255, partial(update_range_vals, dict_ranges = tck_ranges, color = 'B', bound = 'max'))

    while True:
        result, video_frame = video_capture.read()

        mask = apply_mask(video_frame, tck_ranges)
        cv2.imshow(window_name, mask)

        key = cv2.waitKey(5)

        if key == ord('q'):
            break
        elif key == ord('w'):
            data = {'limits': tck_ranges}
            json_file = json.dumps(data, indent=4)
            with open('limits.json', "w") as newFile:
                newFile.write(json_file)
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()