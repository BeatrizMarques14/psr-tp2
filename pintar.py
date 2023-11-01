#!/usr/bin/env python3

import cv2
import argparse
import numpy as np
from functools import partial
from colorama import Fore, Back, Style
import time
import random

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



def cria_zonas(zonas, cores):
    global image_rgb
    height, width, nc = image_rgb.shape


    x_y = random.randint(0,1)                

    font = cv2.FONT_HERSHEY_SIMPLEX 
    org = (50, 50) 
    fontScale = 1
    color = (0, 0, 0) 
    thickness = 2
       
    cores = [1, 2, 3, 4, 5]


    zonas_list = []
    for i in range(zonas):
        x_y = 1 - x_y
        if x_y == 0:
            x_1 = random.randint(20, width-20)
            x_2 = random.randint(20,width-20)
            cv2.line(image_rgb, (x_1, 0), (x_2, height), (0,0,0), 3)

            y = height // 2

            half = (x_1 + x_2) // 2

            zonas_list.append(((x_1,0) ,(x_2,  height)))
        else:
            y_1 = random.randint(20,height-20)
            y_2 = random.randint(20,height-20)

            x = width // 2
            half = (y_2 + y_1) // 2

            cv2.line(image_rgb, (0, y_1), (width, y_2), (0,0,0), 3)
            zonas_list.append(((0, y_1), (width ,y_2)))
    
    image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
    output = cv2.connectedComponentsWithStats(image_gray)
    (numLabels, labels, stats, centroids) = output

    print("CENTOIRDS", centroids)

    l = len(centroids)
    for i in range(1, l):
        (x,y) = centroids[i]
        x1 = int(x) - 5
        y1 = int(y) + 10
        image_rgb = cv2.putText(image_rgb, str(cores[(i+1)//5]), (x1, y1), font,  fontScale, color, thickness, cv2.LINE_AA) 



def main():
    global image_rgb

    window_name = "Imagem"
    pencil_down = [False]
    previous_x = [0]
    previous_y = [0]

    cv2.namedWindow(window_name)

    drawing_data = {'pencil_down' : False, 'previous_x' : 0, 'previous_y': 0, 'color' : (0,0,0), 'draw': 1, 'draw_previous' :1, 'center': (0,0), 'size' : 3}

    cv2.setMouseCallback(window_name, partial(mouseCallback, window_name = window_name, drawing_data = drawing_data))
    cria_zonas(3,4)
    cv2.imshow(window_name, image_rgb)
    
    while True:
        key = cv2.waitKey(50)
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
