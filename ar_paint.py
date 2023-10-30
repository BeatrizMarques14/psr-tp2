#!/usr/bin/env python

import cv2
import numpy as np
import argparse
from functools import partial
from colorama import Fore, Back, Style
from functions import apply_mask
import json

#funcao para detetar os comandos recebidos, chamada a cada instante, tal como a lapis
def comandos():

    #waitkey com um intervalo muito pequeno, mas nao zero
    #deteta a letra
    #manda numero com codigo, que usaremos na de pintar 

    return 0

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



    
    #Mandar a coordenada do centroide

    return centroid_x, centroid_y

#funcao principal, onde se executara o ciclo
def pintar(limits, video_capture, video_name, mask_name, paint_name, canvas):

    while(True):
            result, video_frame = video_capture.read()

            #chama o lapis
            centroid_x, centroid_y = lapis(video_frame,limits, video_name, mask_name)
            
            #so para teste
            key = cv2.waitKey(5)

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

        
        scale = 0.6
        window_width = int(video_frame.shape[1] * scale)
        window_height = int(video_frame.shape[0])

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
        canvas = np.ones((window_height,window_width,3), dtype=np.uint8)*255

        #chama pintar
        pintar(limits, video_capture, video_name, mask_name, paint_name, canvas)
        
            
        return 0
    
    except FileNotFoundError:
        print('Ficheiro não encontrado')

if __name__ == "__main__":
    main()




