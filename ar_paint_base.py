#!/usr/bin/env python3

import cv2
import random
import numpy as np
import argparse
from functools import partial
from colorama import Fore, Back, Style
from functions import apply_mask
import json
import datetime
from PIL import Image

image_original = None 

def mouseCallback(event,x,y,flags,*userdata, image,window_name, drawing_data, shake_detection, video_stream, video_frame):
    drawing_data['coords'] = (x,y)

    if (event == cv2.EVENT_LBUTTONDOWN):
        drawing_data['pencil_down'] = True
        print(Fore.BLUE + 'pencil_down set to True' + Style.RESET_ALL)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing_data['pencil_down'] = False
        print(Fore.RED + 'pencil down released' + Style.RESET_ALL)

    if drawing_data['pencil_down'] == True: 
        pintar_tela(drawing_data, "Paint", image, shake_detection, video_stream)

#funcao para detetar os comandos recebidos, chamada a cada instante, tal como a lapis
def comandos(draw_data, canvas):

    #waitkey com um intervalo muito pequeno, mas nao zero
    #deteta a letra
    #manda numero com codigo, que usaremos na de pintar 

    k = cv2.waitKey(1)

    if k == ord('r'):
        draw_data['cores'] = (0,0,255)
        #draw_data_mouse['cores'] = (0,0,255)
    elif k == ord('g'):
        draw_data['cores'] = (0,255,0)
        #draw_data_mouse['cores'] = (0,255,0)
    elif k == ord('b'):
        draw_data['cores'] = (255,0,0)
        #draw_data_mouse['cores'] = (0,255,0)
    elif k == ord('+'):
        if draw_data['tamanho'] < 50:
            draw_data['tamanho'] = draw_data['tamanho'] + 2
    elif k == ord('-'):
        if draw_data['tamanho'] > 2:
            draw_data['tamanho'] = draw_data['tamanho'] - 2
    elif k == ord('w'):
        now = datetime.datetime.now()
        data_hora = now.strftime("%a_%b_%d_%H:%M:S_%Y")
        filename = f"drawing_{data_hora}.png"
        cv2.imwrite(filename, canvas)
        return 6; #guardar a imagem
    elif k == ord('c'):
        global image_original
        #canvas.fill(255)
        np.copyto(canvas, image_original)
        return k #limpar a imagem
    elif k == ord('a'):
        draw_data['draw'] = 5
        return 5 #retornar aceitacao de circulo ou de retangulo
    elif k == ord('d'):
        draw_data['draw_previous'] = draw_data['draw']
        draw_data['draw'] = 4 #cancel
        return 4 #serve para cancelar, logo retorna um ponto
    elif k == ord('o'):
        print("CIRCULO")
        draw_data['draw_previous'] = draw_data['draw']
        draw_data['draw'] = 2 
        return 2 #comecar circulo
    elif k == ord('s'):
        draw_data['draw_previous'] = draw_data['draw']
        draw_data['draw'] = 3 
        return 3 # retorna quadrado
    else:
        return k #retorna linha

    return k

def shake_prevention(draw_data, paint_name, canvas):

    dx = draw_data['coords'][0] - draw_data['previous_coords'][0]
    dy = draw_data['coords'][1] - draw_data['previous_coords'][1]
    distance = np.sqrt(dx**2 + dy**2)
    if (distance > 250):
        draw_data['draw'] = 4
        #cv2.circle(canvas,draw_data['coords'], draw_data['tamanho'], draw_data['cores'])
        #cv2.imshow(paint_name, canvas)
        return True
    
    return False




def pintar_tela(drawing_data, paint_name, canvas, shake, video_stream, video_frame):
    #paint =
    shake_prevention(drawing_data, paint_name, canvas)
    #if paint == False:
    #    cv2.line(canvas,draw_data['previous_coords'], draw_data['coords'], draw_data['cores'], draw_data['tamanho'])
    show = canvas

    if drawing_data['draw'] == 1:
        cv2.line(canvas, (drawing_data['previous_coords'][0], drawing_data['previous_coords'][1]), drawing_data['coords'], drawing_data['cores'], drawing_data['tamanho'])
        drawing_data['previous_coords'] = drawing_data['coords']
    elif drawing_data['draw'] in (2, 3): #save the pivot point for the circle/square
        drawing_data['draw_previous'] = drawing_data['draw']
        drawing_data['draw'] = 6
        drawing_data['previous_coords'] = drawing_data['coords']
    elif drawing_data['draw'] == 4: #desenhar um ponto
        cv2.circle(canvas, drawing_data['coords'], drawing_data['tamanho']//2, drawing_data['cores'], -1) #depois o raio do circulo vai depender do tamanho
        drawing_data['draw'] = 1
        drawing_data['previous_coords'] = drawing_data['coords']
    elif drawing_data['draw'] == 5: #circulo foi aceite, colocar depois acao anterior para verificar se era mesmo um circulo
        print("previous", drawing_data['previous_coords'])
        print("now", drawing_data['coords'])
        if drawing_data['draw_previous'] == 3:
            cv2.rectangle(canvas, (drawing_data['previous_coords'][0], drawing_data['previous_coords'][1]), drawing_data['coords'], drawing_data['cores'], drawing_data['tamanho'])
        elif drawing_data['draw_previous'] == 2:
            dist = int(np.sqrt( (drawing_data['previous_coords'][0] - drawing_data['coords'][0]) ** 2 + (drawing_data['previous_coords'][1] - drawing_data['coords'][1]) ** 2))
            cv2.circle(canvas, (drawing_data['previous_coords'][0], drawing_data['previous_coords'][1]), dist, drawing_data['cores'], drawing_data['tamanho'])
        drawing_data['draw'] = 4
        drawing_data['previous_coords'] = drawing_data['coords']
    elif drawing_data['draw'] == 6:
        print("HERE", drawing_data['previous_coords'])
        img_cpy = np.copy(canvas)
        if drawing_data['draw_previous'] == 3:
            cv2.rectangle(img_cpy, (drawing_data['previous_coords'][0], drawing_data['previous_coords'][1]), drawing_data['coords'], drawing_data['cores'], drawing_data['tamanho'])
        elif drawing_data['draw_previous'] == 2:
            dist = int(np.sqrt( (drawing_data['previous_coords'][0] - drawing_data['coords'][0]) ** 2 + (drawing_data['previous_coords'][1] - drawing_data['coords'][1]) ** 2))
            cv2.circle(img_cpy, (drawing_data['previous_coords'][0], drawing_data['previous_coords'][1]), dist, drawing_data['cores'], drawing_data['tamanho'])
        show = img_cpy


    if video_stream:
        canvas_video = video_frame.copy()
        mask_b = cv2.inRange(show, (0,0,0), (255,0,0))
        mask_g = cv2.inRange(show, (0,255,0), (0,255,0))
        mask_r = cv2.inRange(show, (0,0,255), (0,0,255))

        canvas_video[mask_b>0] = (255,0,0)
        canvas_video[mask_g>0] = (0,255,0)
        canvas_video[mask_r>0] = (0,0,255)

        cv2.imshow(paint_name, canvas_video)

    else:
        cv2.imshow(paint_name, show)


#lapis vai detetar e dar a posicao do lapis, sem ser filtrada
def lapis(video_frame, limits, video_name, mask_name):
    #Recebe imagem da camara
    #Aplica os limites
    mask = apply_mask(video_frame, limits)
    #Mostrar a imagem original e a transformada
    cv2.imshow(video_name, video_frame)
    cv2.imshow(mask_name, mask)
    #Mostrar imagemm com o objeto maior, e colocar a verde na imagem original
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask)
    if num_labels > 1:

        # Encontra o rótulo do maior componente (excluindo o componente de fundo)
        largest_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1

        if stats[largest_label][cv2.CC_STAT_AREA] >= 100:

            # Crie uma nova máscara com base no maior componente
            largest_mask = np.zeros_like(mask)
            largest_mask[labels == largest_label] = 255

            # Defina a cor verde para a máscara do maior componente
            largest_mask_color = cv2.merge((np.zeros_like(largest_mask), largest_mask, np.zeros_like(largest_mask)))

            # Sobreponha a máscara na imagem original
            result = cv2.addWeighted(video_frame, 1, largest_mask_color, 1, 0)

            # Exiba a imagem resultante
            cv2.imshow(video_name, result)

            centroid_x = int(centroids[largest_label][0])
            centroid_y = int(centroids[largest_label][1])

                #Colocar cruz vermelha no centroide da imagem original
            cv2.circle(result,(centroid_x,centroid_y),10,(0,0,255),-1)
            cv2.imshow(video_name,result)
        else:
            centroid_x = -1
            centroid_y = -1

    else:

        centroid_x = -1
        centroid_y = -1
    
    return centroid_x, centroid_y

def cria_zonas(zonas):
    global image_original
    height, width, nc = image_original.shape


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
            cv2.line(image_original, (x_1, 0), (x_2, height), (0,0,0), 3)

            y = height // 2

            half = (x_1 + x_2) // 2

            zonas_list.append(((x_1,0) ,(x_2,  height)))
        else:
            y_1 = random.randint(20,height-20)
            y_2 = random.randint(20,height-20)

            x = width // 2
            half = (y_2 + y_1) // 2

            cv2.line(image_original, (0, y_1), (width, y_2), (0,0,0), 3)
            zonas_list.append(((0, y_1), (width ,y_2)))
    
    image_gray = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)
    output = cv2.connectedComponentsWithStats(image_gray)
    (numLabels, labels, stats, centroids) = output

    print("CENTOIRDS", centroids)

    l = len(centroids)
    for i in range(1, l):
        (x,y) = centroids[i]
        x1 = int(x) - 5
        y1 = int(y) + 10
        image_rgb = cv2.putText(image_original, str(cores[(i+1)//5]), (x1, y1), font,  fontScale, color, thickness, cv2.LINE_AA) 


#funcao principal, onde se executara o ciclo
def pintar(limits, video_capture, video_name, mask_name, paint_name, canvas, shake,video_stream, video_frame):

    draw_data = {'cores' : (0,0,0), # comeca a preto
                 'tamanho' : 3, #3 pixeis inicialmente, depois ver se e muito 
                 'draw': 0, 
                 'draw_previous': 0,
                 'centro': (-1,-1), #-coordenadas do ponto inicial do quadrado ou elipse ou linha
                 'coords': (-1,-1), #coordenadas do centroide atuais
                 'previous_coords' : (-1,-1), #coordenadas do centroide anteriores
                 'pencil_down':False
           }
    #drawing_data_mouse = {'pencil_down' : False, 'coords' : (0,0), 'previous_coords':(-1,-1), 'cores': draw_data['cores'] , 'tamanho': draw_data['tamanho']}
    cv2.setMouseCallback(video_name, partial(mouseCallback, image = canvas, window_name = paint_name, drawing_data = draw_data, shake_detection = shake, video_stream=video_stream, video_frame=video_frame))


    while(True):
            result, video_frame = video_capture.read()
            

            #chama o lapis
            #draw_data['previous_coords'] = draw_data['coords']
            coords = lapis(video_frame,limits, video_name, mask_name)
            draw_data['coords'] = coords
            print(draw_data['coords'])
            print(draw_data['previous_coords'])

            key = comandos(draw_data, canvas)
            #if paint == False:
            pintar_tela(draw_data, paint_name, canvas, shake, video_stream, video_frame)

            
            #so para teste
            #key = cv2.waitKey(5)

            if key == ord('q'):
                break
    
    #chama o shake detection para corrigir a posicao do lapis
    #caso ocorra o evento de usarmos o rato, atualiza novamente a posicao do lapis

    #chama a comandos
    #verifica o codigo que recebemos
    #se for algo tratar aqui

    #pintar a tela



    return 0


def main() :

    #Recebe argumentos
    #-j JSON ou --json JSON
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json', type=str, required=True,help='Full path to json file.')
    parser.add_argument('-usp', '--use_shake_prevention', help = 'Use shake prevention', action = 'store_true')
    parser.add_argument('-vs', '--use_video_stream', help = 'instead of using a white board, use the video as your canvas', action = 'store_true')
    args = vars(parser.parse_args())

    #Ler os limites de la
    try:
        with open(args['json'], 'r') as openfile:
            json_file = json.load(openfile)
            limits = json_file['limits']
        
        shake = args['use_shake_prevention']
        video_stream = args['use_video_stream']
        

    
        #Ver o tamanho das imagens da camara
        video_capture = cv2.VideoCapture(0)
        result, video_frame = video_capture.read()

        
        scale = 0.5
        window_width = int(video_frame.shape[1] * scale)
        window_height = int(video_frame.shape[0]*scale)

        video_name = 'Video'
        cv2.namedWindow(video_name,cv2.WINDOW_NORMAL)
        cv2.resizeWindow(video_name, window_width, window_height)

        mask_name = 'Mask'
        cv2.namedWindow(mask_name,cv2.WINDOW_NORMAL)
        cv2.resizeWindow(mask_name, window_width, window_height)

        paint_name = 'Paint'
        cv2.namedWindow(paint_name,cv2.WINDOW_NORMAL)
        cv2.resizeWindow(paint_name, window_width, window_height)

        #Criar tela
        global image_original
        image_original = np.ones((video_frame.shape[0],video_frame.shape[1],3), dtype=np.uint8)*255

        cria_zonas(3)

        canvas = np.copy(image_original) 
        #np.ones((video_frame.shape[0],video_frame.shape[1],3), dtype=np.uint8)*255


        cv2.imshow(paint_name, canvas)

        
        #chama pintar
        pintar(limits, video_capture, video_name, mask_name, paint_name, canvas, shake, video_stream, video_frame)
        
            
        return 0
    
    except FileNotFoundError:
        print('Ficheiro não encontrado')

if __name__ == "__main__":
    main()




