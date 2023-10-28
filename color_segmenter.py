#!/usr/bin/env python
import cv2
import numpy as np
import argparse
from functools import partial
from colorama import Fore, Style



def onTrackbar(min_val,max_val, image, window_name):
    
    _,tresh = cv2.threshold(image, min_val, max_val, cv2.THRESH_BINARY)
    cv2.imshow(window_name, tresh)



def main():


    # Initialization
    blue_image = {'image': None,'min_val':0, 'max_val':255}
    green_image = {'image': None,'min_val':0, 'max_val':255}
    red_image = {'image': None,'min_val':0, 'max_val':255}



    capture = cv2.VideoCapture(0)
    _, image = capture.read()  # get an image from the camera
    [blue_image['image'], green_image['image'], red_image['image']] = cv2.split(image)  #split the image in the 3 bgr channels
    window_name = 'Video'
    mask_name = 'Mask'
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name,800,600)
    cv2.namedWindow(mask_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(mask_name, 800,900)

    #Criar as trakbars para o azul
    cv2.createTrackbar('Bmin (0,255)', mask_name, 0, 255, partial(onTrackbar, max_val = 255,image = blue_image['image'], window_name = mask_name))
    cv2.createTrackbar('Bmax (0,255)', mask_name, 0, 255, partial(onTrackbar, max_val = 255,image = blue_image['image'], window_name = mask_name))
    
    #Criar as trakbars para o verde
    cv2.createTrackbar('Gmin (0,255)', mask_name, 0, 255, partial(onTrackbar, max_val = 255, image = green_image['image'], window_name = mask_name))
    cv2.createTrackbar('Gmax (0,255)', mask_name, 0, 255, partial(onTrackbar, max_val = 255, image = green_image['image'], window_name = mask_name))

    #Criar as trakbars para o vermelho
    cv2.createTrackbar('Rmin (0,255)', mask_name, 0, 255, partial(onTrackbar, max_val = 255, image = red_image['image'], window_name = mask_name))
    cv2.createTrackbar('Rmax (0,255)', mask_name, 0, 255, partial(onTrackbar, max_val = 255, image = red_image['image'], window_name = mask_name))

    #colocar as trakbars no valor minimo e maximo
    cv2.setTrackbarPos('Bmin (0,255)',mask_name, blue_image['min_val'])
    cv2.setTrackbarPos('Bmax (0,255)',mask_name, blue_image['max_val'])

    cv2.setTrackbarPos('Gmin (0,255)',mask_name, green_image['min_val'])
    cv2.setTrackbarPos('Gmax (0,255)',mask_name, green_image['max_val'])

    cv2.setTrackbarPos('Rmin (0,255)',mask_name, red_image['min_val'])
    cv2.setTrackbarPos('Rmax (0,255)',mask_name, red_image['max_val'])


    #Execution
    while True:
        _, image = capture.read()  # get an image from the camera
        [blue_image['image'], green_image['image'], red_image['image']] = cv2.split(image)  #split the image in the 3 bgr channels

        #verifica os valores das trackbars
        blue_image['min_val'] = cv2.getTrackbarPos('Bmin (0,255)', mask_name)
        blue_image['max_val'] = cv2.getTrackbarPos('Bmax (0,255)', mask_name)

        green_image['min_val'] = cv2.getTrackbarPos('Gmin (0,255)', mask_name)
        green_image['max_val'] = cv2.getTrackbarPos('Gmax (0,255)', mask_name)

        red_image['min_val'] = cv2.getTrackbarPos('Rmin (0,255)', mask_name)
        red_image['max_val'] = cv2.getTrackbarPos('Rmax (0,255)', mask_name)
        
    

        # Visualization

        cv2.imshow(window_name, image)
        
        #aplica os tresholds
        onTrackbar(blue_image['min_val'], blue_image['max_val'], blue_image['image'],mask_name)
        onTrackbar(green_image['min_val'], green_image['max_val'], green_image['image'],mask_name)
        onTrackbar(red_image['min_val'], red_image['max_val'], red_image['image'],mask_name)

        key = cv2.waitKey(25)
        if key == ord('w'):
            break


if __name__ == '__main__':
    main()