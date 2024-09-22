# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 19:10:52 2024

@author: x
"""

import json      #Para almacenar el conocimiento
import os        #Para interactuar con el sistema operativo. Para crear archivos
import re        #Limpia cadenas de texto
from fuzzywuzzy import fuzz #Medimos la similitud entre cadenas.                            


# Archivo donde se almacenará el conocimiento
FILE_PATH = "conocimiento.json"

# Umbral de similitud para considerar una entrada como similar
SIMILARITY_THRESHOLD = 75

# Cargar o inicializar la base de conocimiento
def cargar_conocimiento():
    if os.path.exists(FILE_PATH): #Revisa si existe el archivo
        with open(FILE_PATH, "r") as file: #Se abre en modo de lectura "r"
                                           #Se cierra al salir del módulo con with
            return json.load(file)         #Devuelve el diccionario cargado
    else:
        # Conocimiento inicial
        return {
            "Hola": "¡Hola! Haz tu pregunta",
            "¿Cómo estás?": "Estoy bien, gracias. Haz tu pregunta",
            "¿De qué te gustaría hablar?": "Puedes preguntar lo que quieras, ¡tú decides!"
        }

# Guardar el conocimiento actualizado en el archivo
def guardar_conocimiento(conocimiento):         #Recibe un diccionario
    with open(FILE_PATH, "w") as file:          #Abre escribe la nueva información
        json.dump(conocimiento, file, indent=4)

# Normalizar el texto: minúsculas y sin puntuación
def normalizar_texto(texto):
    texto = texto.lower() #se convierte a minúsculas
    texto = re.sub(r'[^\w\s]', '', texto)  # Eliminar puntuación que no sea un caracter o espacio
    return texto 


# Función para buscar una entrada similar en el diccionario de conocimiento usando Token Sort Ratio
def buscar_similar(user_input, conocimiento): #Toma la entrada y el diccionario
    user_input_normalizado = normalizar_texto(user_input) #Normaliza con una funcion
    mejor_match = None #Se crea variable vacia
    mejor_similitud = 0 #Se crea variable vacia
    
    # Comparar con cada entrada del conocimiento
    for pregunta, respuesta in conocimiento.items(): #itera sobre la pregunta y la respuesta en el dicionario
        pregunta_normalizada = normalizar_texto(pregunta) #Se normaliza la pregunta del diccionario
        #para calcular la similitud entre la entrada del usuario y la pregunta normalizada.
        similitud = fuzz.token_sort_ratio(user_input_normalizado, pregunta_normalizada)
            #La funcion puede ir de 0 a 100
        
        if similitud > mejor_similitud: #Si similitud es mayor a la mejor similitud
            mejor_similitud = similitud #La mejor similitud es la actual
            mejor_match = pregunta      #El mejor match es ka pregunta actual

    # Si la similitud es suficientemente alta, devolver el mejor match
    if mejor_similitud >= SIMILARITY_THRESHOLD:
        return mejor_match #Regresa la pregunta que encontró en diccionario
    else:
        return None #No regresa nada
    
def chat():
    conocimiento = cargar_conocimiento()  # Se guarda el conocimiento previo
    
    while True:
        # Leer entrada del usuario
        user_input = input("\nUsuario: ").strip()  # Toma la entrada y elimina espacios en blanco
        
        # Normalizar la entrada del usuario
        user_input_normalizado = normalizar_texto(user_input)
        
        # Buscar una entrada similar en el diccionario de conocimiento
        similar_input = buscar_similar(user_input_normalizado, conocimiento)  # Usar la entrada normalizada
        
        if similar_input:
            print(f"Bot: {conocimiento[similar_input]}")  # Da la respuesta
        else:
            # Si no se encuentra la respuesta, preguntar al usuario
            print(f"Bot: No sé cómo responder a eso.")
            nueva_respuesta = input("Por favor, enséñame cómo debería responder a esa pregunta: ").strip()
            
            # Añadir el nuevo conocimiento al diccionario con la pregunta normalizada
            conocimiento[user_input_normalizado] = nueva_respuesta
            guardar_conocimiento(conocimiento)  # Guardar los cambios en el archivo
            
            print("Bot: ¡Gracias! Ahora sé un poco más.")

# Ejecutar el chat
if __name__ == "__main__":
    chat()