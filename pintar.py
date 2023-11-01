#!/usr/bin/env python3

import cv2
import argparse
import numpy as np
from functools import partial
from colorama import Fore, Back, Style
import time

height = 480
width = 640

image_rgb = np.ones((height, width, 3), dtype=np.uint8)*255

def mouseCallback(event, x, y, flags, *userdata, window_name, drawing_data):
    global image_rgb
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing_data['pencil_down'] = True
        print(Fore.BLUE + "pencil down is set" + Style.RESET_ALL)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing_data['pencil_down'] = False
        print(Fore.RED + "pencil down is unset" + Style.RESET_ALL)
    if drawing_data['pencil_down'] == True:
        draw(image_rgb, window_name, (x,y), drawing_data)


def draw(image_rgb, window_name, pos, drawing_data):
    (x,y) = pos
    if drawing_data['draw'] == 1:
        cv2.line(image_rgb, (drawing_data['previous_x'], drawing_data['previous_y']), (x, y), drawing_data['color'], drawing_data['size'])
    elif drawing_data['draw'] in (2, 3): #save the pivot point for the circle/square
        drawing_data['draw_previous'] = drawing_data['draw']
        drawing_data['draw'] = 6
    elif drawing_data['draw'] == 4: #desenhar um ponto
        cv2.circle(image_rgb, (x, y), drawing_data['size']//2, drawing_data['color'], -1) #depois o raio do circulo vai depender do tamanho
        drawing_data['draw'] = 1
    elif drawing_data['draw'] == 5: #circulo foi aceite, colocar depois acao anterior para verificar se era mesmo um circulo
        if drawing_data['draw_previous'] == 3:
            cv2.rectangle(image_rgb, (drawing_data['previous_x'], drawing_data['previous_y']), (x,y), drawing_data['color'], drawing_data['size'])
        elif drawing_data['draw_previous'] == 2:
            dist = int(np.sqrt( (drawing_data['previous_x'] - x) ** 2 + (drawing_data['previous_y'] - y) ** 2))
            cv2.circle(image_rgb, (drawing_data['previous_x'], drawing_data['previous_y']), dist, drawing_data['color'], drawing_data['size'])
        drawing_data['draw'] = 4
    elif drawing_data['draw'] == 6:
        img_cpy = np.copy(image_rgb)
        if drawing_data['draw_previous'] == 3:
            cv2.rectangle(img_cpy, (drawing_data['previous_x'], drawing_data['previous_y']), (x,y), drawing_data['color'], drawing_data['size'])
        elif drawing_data['draw_previous'] == 2:
            dist = int(np.sqrt( (drawing_data['previous_x'] - x) ** 2 + (drawing_data['previous_y'] - y) ** 2))
            cv2.circle(img_cpy, (drawing_data['previous_x'], drawing_data['previous_y']), dist, drawing_data['color'], drawing_data['size'])
        cv2.imshow(window_name, img_cpy)
        return

    cv2.imshow(window_name, image_rgb)
    drawing_data['previous_x'] = x
    drawing_data['previous_y'] = y



def main():
    global image_rgb

    window_name = "Imagem"
    pencil_down = [False]
    previous_x = [0]
    previous_y = [0]

    cv2.namedWindow(window_name)

    drawing_data = {'pencil_down' : False, 'previous_x' : 0, 'previous_y': 0, 'color' : (0,0,0), 'draw': 1, 'draw_previous' :1, 'center': (0,0), 'size' : 3}

    cv2.setMouseCallback(window_name, partial(mouseCallback, window_name = window_name, drawing_data = drawing_data))
    cv2.imshow(window_name, image_rgb)
    
    while True:
        key = cv2.waitKey(50)
        print(key)
        #if(key == -1):
            #cv2.imshow(window_name, image)
        if key == ord('q'):
            print("quiting")
            break
        elif key == ord('p'): 
            print("setting pencil to white color")
            drawing_data['color'] = (255, 255, 255)
        elif key == ord('n'):
            print("setting pencil to black(no) color")
            drawing_data['color'] = (0, 0 ,0)

        elif key == ord('r'): # red color for pencil
            print("setting pencil to red color")
            drawing_data['color'] = (0, 0 ,255)

        elif key == ord('g'):
            print("setting pencil to green color")
            drawing_data['color'] = (0, 255 ,0)
        elif key == ord('b'):
            print("setting pencil to blue color")
            drawing_data['color'] = (255, 0 ,0)
        elif key == ord('s'):
            print("setting pencil to square")
            drawing_data['draw_previous'] = drawing_data['draw']
            drawing_data['draw'] = 3 
        elif key == ord('o'):
            print("setting pencil to circle")
            drawing_data['draw_previous'] = drawing_data['draw']
            drawing_data['draw'] = 2 
        elif key == ord('d'):
            drawing_data['draw_previous'] = drawing_data['draw']
            drawing_data['draw'] = 4 #cancel
        elif key == ord('a'):
            #drawing_data['draw_previous'] = drawing_data['draw']
            drawing_data['draw'] = 5 #accetp
        elif key == ord('+'):
            new_size = drawing_data['size'] + 5
            drawing_data['size'] = min(new_size, 33)
        elif key == ord('-'):
            new_size = drawing_data['size'] - 5
            drawing_data['size'] = max(new_size, 4)
        elif key == ord('c'):
            image_rgb = np.ones((height, width, 3), dtype=np.uint8)*255
        elif key == ord('w'):
            filename = "drawing" + str(time.ctime()) + ".png"
            cv2.imwrite(filename, image_rgb)

    cv2.destroyWindow(window_name)

if __name__ == "__main__":
    main()
