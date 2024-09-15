# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 12:31:30 2024

@author: x
"""
import numpy as np

def PERCEPTRON_SISTEMA_SEGURIDAD(X, Y):
    # Inicializamos los pesos en ceros para los tres elementos (incluyendo el sesgo)
    W = np.array([0, 0, 0])
    
    # Iteramos para entrenar el perceptrón con los 4 ejemplos de la tabla de verdad
    for n in range(4):
        
        # Transponemos W y hacemos el producto punto con la fila de entradas X[n]
        WT = np.transpose(W)
        y_testada = np.dot(WT, X[n, :])
        
        # Clasificamos la salida; si el valor es menor que 0, lo clasificamos como 0
        if y_testada < 0:
            y_testada = 0
        else:
            y_testada = 1  # Si el valor es mayor o igual a 0, clasificamos como 1
        
        # Ajustamos los pesos: W = W + (tasa de aprendizaje) * (error) * entrada
        W = W + 0.5 * (Y[n] - y_testada) * X[n, :]
        print(f"Pesos ajustados en la iteración {n+1}: {W}")
    
    # Al final retornamos los pesos ajustados
    return W




# Tabla de verdad para dos sensores en un sistema de seguriad de una casa

#   Salida |sensor A| sensor B

X = np.array([[1, 0, 0],  # Ambos sensores (puerta y ventana) están cerrados
              [1, 0, 1],  # Puerta cerrada, ventana abierta
              [1, 1, 0],  # Puerta abierta, ventana cerrada
              [1, 1, 1]]) # Ambos sensores abiertos

# Salidas esperadas según la tabla de verdad OR: Alarma se activa si al menos un sensor detecta intrusión
Y = np.array([0, 1, 1, 1])

# Llamamos a la función para entrenar el perceptrón
Final = PERCEPTRON_SISTEMA_SEGURIDAD(X, Y)

# Mostramos los pesos finales que ha aprendido el perceptrón
print(f"Pesos finales aprendidos: {Final}")
