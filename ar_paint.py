#!/usr/bin/env python

import cv2
import numpy as np
import argparse
from functools import partial
from colorama import Fore, Back, Style

#funcao para detetar os comandos recebidos, chamada a cada instante, tal como a lapis
def comandos():

    #waitkey com um intervalo muito pequeno, mas nao zero
    #deteta a letra
    #manda numero com codigo, que usaremos na de pintar 

    return 0

#lapis vai detetar e dar a posicao do lapis, sem ser filtrada
def lapis():
    #Recebe imagem da camara
    #Aplica os limites
    #Mostrar a imagem original e a transformada
    #Mostrar imagemm com o objeto maior, e colocar a verde na imagem original
    #Calcular centroide objeto
    #Colocar cruz vermelha no centroide da imagem original
    #Mandar a coordenada do centroide

    return 0

#funcao principal, onde se executara o ciclo
def pintar():
    #chama o lapis
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

    #Ler os limites de la
    #Ver o tamanho das imagens da camara
    #Criar tela

    #chama pintar
    return 0

if __name__ == "__main__":
    main()


