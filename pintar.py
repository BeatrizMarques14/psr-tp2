#!/usr/bin/env python3

import cv2
import argparse
import numpy as np
from functools import partial
from colorama import Fore, Back, Style


def mouseCallback(event, x, y, flags, *userdata, image_rgb, window_name, drawing_data):
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing_data['pencil_down'] = True
        print(Fore.BLUE + "pencil down is set" + Style.RESET_ALL)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing_data['pencil_down'] = False
        print(Fore.RED + "pencil down is unset" + Style.RESET_ALL)
    if drawing_data['pencil_down'] == True:
        if drawing_data['draw'] == 1:
            cv2.line(image_rgb, (drawing_data['previous_x'], drawing_data['previous_y']), (x, y), drawing_data['color'], 2)
        elif drawing_data['draw'] == 2:
            drawing_data['previous_x'] = x
            drawing_data['previous_y'] = y
            drawing_data['draw'] = 6
            cv2.imshow(window_name, image_rgb)
            return
        elif drawing_data['draw'] == 4:
            cv2.circle(image_rgb, (x, y), 3, drawing_data['color'], -1) #depois o raio do circulo vai depender do tamanho
            drawing_data['draw'] = 1

        elif drawing_data['draw'] == 5: #circulo foi aceite, colocar depois acao anterior para verificar se era mesmo um circulo
            dist = int(np.sqrt( (drawing_data['previous_x'] - x) ** 2 + (drawing_data['previous_y'] - y) ** 2))
            cv2.circle(image_rgb, (drawing_data['previous_x'], drawing_data['previous_y']), dist, drawing_data['color'], 2)
            cv2.imshow(window_name, image_rgb)
            drawing_data['draw'] = 6
            return
        elif drawing_data['draw'] == 6:
            img_cpy = np.copy(image_rgb)
            print(img_cpy != image_rgb)
            dist = int(np.sqrt( (drawing_data['previous_x'] - x) ** 2 + (drawing_data['previous_y'] - y) ** 2))
            cv2.circle(img_cpy, (drawing_data['previous_x'], drawing_data['previous_y']), dist, drawing_data['color'], 2)
            cv2.imshow(window_name, img_cpy)
            return
    cv2.imshow(window_name, image_rgb)
    drawing_data['previous_x'] = x
    drawing_data['previous_y'] = y



def main():
    #---------
    #Inicializacao
    #----------------


    window_name = "Imagem"
    pencil_down = [False]
    previous_x = [0]
    previous_y = [0]

    #parser = argparse.ArgumentParser()
    #parser.add_argument('-i', '--image', type=str, default = image_name,help='Full path to image file.')
    #args = vars(parser.parse_args())

    #Open image
    height = 480
    width = 640

    image = np.ones((height, width, 3), dtype=np.uint8)*255

    cv2.namedWindow(window_name)

    drawing_data = {'pencil_down' : False, 'previous_x' : 0, 'previous_y': 0, 'color' : (0,0,0), 'draw': 1, 'center': (0,0)}

    cv2.setMouseCallback(window_name, partial(mouseCallback, image_rgb = image, window_name = window_name, drawing_data = drawing_data))

    #---------
    #Execucao
    #----------------

    #Circle Variables
    height, width, channels = image.shape
    center = (width // 2, height // 2)

    #Add circle to image
    cv2.imshow(window_name, image)
    
    #---------------
    # Visualizacao
    #----------------
    while True:
        key = cv2.waitKey(50)
        print(key)
        #if(key == -1):
            #cv2.imshow(window_name, image)
        if key == ord('q'):
            print("quiting")
            break
        elif key == ord('w'): 
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
            drawing_data['draw'] = 3 
        elif key == ord('o'):
            print("setting pencil to circle")
            drawing_data['draw'] = 2 
        elif key == ord('d'):
            drawing_data['draw'] = 4 #cancel
        elif key == ord('a'):
            drawing_data['draw'] = 5 #accetp
        elif key == ord('c'):
            image = np.ones((height, width, 3), dtype=np.uint8)*255

    cv2.destroyWindow(window_name)

if __name__ == "__main__":
    main()