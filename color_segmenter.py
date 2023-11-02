#!/usr/bin/env python3
import cv2
import numpy as np
import argparse
from functools import partial
from colorama import Fore, Style

def onTrackbar(val, params, window_name):
    # Atualize os valores no dicionário 'params'
    params['min_R'] = cv2.getTrackbarPos('Min_R', window_name)
    params['min_G'] = cv2.getTrackbarPos('Min_G', window_name)
    params['min_B'] = cv2.getTrackbarPos('Min_B', window_name)
    params['max_R'] = cv2.getTrackbarPos('Max_R', window_name)
    params['max_G'] = cv2.getTrackbarPos('Max_G', window_name)
    params['max_B'] = cv2.getTrackbarPos('Max_B', window_name)

    min_values = np.array([params['min_B'], params['min_G'], params['min_R']], dtype=np.uint8)
    max_values = np.array([params['max_B'], params['max_G'], params['max_R']], dtype=np.uint8)

    mask = cv2.inRange(params['frame'], min_values, max_values)
    cv2.imshow(window_name, mask)

# Crie uma janela para exibir a imagem
window_name = 'Segmented Image'
cv2.namedWindow('Segmented Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Segmented Image', 600, 900)

# Inicialize os limites iniciais (R, G, B mínimos e máximos)
val = 0
params = {'frame': None, 'min_B': 0, 'min_G': 0, 'min_R': 0, 'max_B': 255, 'max_G': 255, 'max_R': 255}


# Inicialize a captura de vídeo da câmera (use 0 para a câmera padrão)
cap = cv2.VideoCapture(0)
_, params['frame'] = cap.read()

# Crie trackbars para ajustar os limites
cv2.createTrackbar('Min_R', 'Segmented Image', 0, 255, partial(onTrackbar, params=params, window_name=window_name))
cv2.createTrackbar('Min_G', 'Segmented Image', 0, 255, partial(onTrackbar, params=params, window_name=window_name))
cv2.createTrackbar('Min_B', 'Segmented Image', 0, 255, partial(onTrackbar, params=params, window_name=window_name))
cv2.createTrackbar('Max_R', 'Segmented Image', 255, 255, partial(onTrackbar, params=params, window_name=window_name))
cv2.createTrackbar('Max_G', 'Segmented Image', 255, 255, partial(onTrackbar, params=params, window_name=window_name))
cv2.createTrackbar('Max_B', 'Segmented Image', 255, 255, partial(onTrackbar, params=params, window_name=window_name))

cv2.setTrackbarPos('Max_B',window_name,255)

while True:
    # Captura um quadro da câmera
    _, params['frame'] = cap.read()

    onTrackbar(val, params, window_name)

    # Exiba a imagem da máscara
    key = cv2.waitKey(25)
    if key == ord('w'):
        {'limits': {'B': {'max': params['max_B'], 'min': params['min_B']},
            'G': {'max': params['max_G'], 'min': params['min_G']},
            'R': {'max': params['max_R'], 'min': params['min_R']}}}
        break

# Libere a câmera e feche todas as janelas
cap.release()
cv2.destroyAllWindows()
