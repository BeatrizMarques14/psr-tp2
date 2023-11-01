#!/usr/bin/env python

import cv2
import numpy as np
import argparse
from functools import partial
from colorama import Fore, Back, Style
from functions import apply_mask
import json
import datetime

#funcao para detetar os comandos recebidos, chamada a cada instante, tal como a lapis
def comandos(draw_data, canvas):

    #waitkey com um intervalo muito pequeno, mas nao zero
    #deteta a letra
    #manda numero com codigo, que usaremos na de pintar 

    k = cv2.waitKey(1)

    if k == ord('r'):
        draw_data['cores'] = (0,0,255)
    elif k == ord('g'):
        draw_data['cores'] = (0,255,0)
    elif k == ord('b'):
        draw_data['cores'] = (255,0,0)
    elif k == ord('+'):
        if draw_data['tamanho'] < 100:
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
        canvas.fill(255)
        return 5 #limpar a imagem
    elif k == ord('a'):
        return 4 #retornar aceitacao de circulo ou de retangulo
    elif k == ord('d'):
        return 1 #serve para cancelar, logo retorna um ponto
    elif k == ord('o'):
        return 3 #comecar circulo
    elif k == ord('s'):
        return 2 # retorna quadrado
    else:
        return k #retorna linha

    return k

def pintar_tela(draw_data, paint_name, canvas):
    cv2.line(canvas,draw_data['previous_coords'], draw_data['coords'], draw_data['cores'], draw_data['tamanho'])
    cv2.imshow(paint_name, canvas)


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

        # Encontre o rótulo do maior componente (excluindo o componente de fundo)
        largest_label = np.argmax(stats[1:, cv2.CC_STAT_AREA]) + 1

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
    
    return centroid_x, centroid_y

#funcao principal, onde se executara o ciclo
def pintar(limits, video_capture, video_name, mask_name, paint_name, canvas):

    draw_data = {'cores' : (0,0,0), # comeca a preto
                 'tamanho' : 3, #3 pixeis inicialmente, depois ver se e muito 
                 'action': 0, 
                 'centro': (-1,-1), #-coordenadas do ponto inicial do quadrado ou elipse ou linha
                 'coords': (-1,-1), #coordenadas do centroide atuais
                 'previous_coords' : (-1,-1) #coordenadas do centroide anteriores
           }

    while(True):
            result, video_frame = video_capture.read()

            #chama o lapis
            draw_data['previous_coords'] = draw_data['coords']
            coords = lapis(video_frame,limits, video_name, mask_name)
            draw_data['coords'] = coords

            key = comandos(draw_data, canvas)
            pintar_tela(draw_data, paint_name, canvas)
            
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
    args = vars(parser.parse_args())

    #Ler os limites de la
    try:
        with open(args['json'], 'r') as openfile:
            json_file = json.load(openfile)
            limits = json_file['limits']
        

    
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
        canvas = np.ones((video_frame.shape[0],video_frame.shape[1],3), dtype=np.uint8)*255

        cv2.imshow(paint_name, canvas)
        #chama pintar
        pintar(limits, video_capture, video_name, mask_name, paint_name, canvas)
        
            
        return 0
    
    except FileNotFoundError:
        print('Ficheiro não encontrado')

if __name__ == "__main__":
    main()


