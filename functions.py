#!/usr/bin/env python


import cv2
import numpy as np

def centroid_pos(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if contours:
        biggest_area = max(contours, cv2.contourArea)

        selected_area = np.zeros(mask.shape, np.uint8)
        cv2.drawContours(selected_area, biggest_area, -1, (0,255,0), cv2.FILLED)
        selected_area = cv2.bitwise_and(mask, selected_area)
        areas_noise = cv2.bitwise_xor(mask, selected_area)

        frame = cv2.merge([areas_noise,mask,areas_noise])

        moments = cv2.moments(biggest_area)
        if moments["m00"] != 0:
            coord_x = int(moments['m10']/moments['m00'])
            coord_y = int(moments['m01']/moments['m00'])

            frame = cv2.putText(frame, 'X', [coord_x, coord_y], cv2.FONT_HERSHEY_SIMPLEX, 2, cv2.LINE_AA)

            return (coord_x, coord_y), frame
    else:
        frame = cv2.merge([mask,mask,mask])
        return (None, None), frame




def update_range_vals(val, dict_ranges, color, bound):
    dict_ranges[color][bound] = val


def apply_mask(img, dict_ranges):
    mins = dict_ranges['B']['min'], dict_ranges['G']['min'], dict_ranges['R']['min']
    maxs = dict_ranges['B']['max'], dict_ranges['G']['max'], dict_ranges['R']['max']

    return cv2.inRange(img, mins, maxs)