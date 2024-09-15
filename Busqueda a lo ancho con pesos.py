import pandas as pd
from collections import deque

# Valores del grafo
V = ['Casa', 'Copalita', 'Sta Sofia', 'Guadalajara', 'Juan Gil Preciado', 
     'Angel Leano', 'Valdepenas', 'Arco del triunfo', 'La cima']

# Matriz de adyacencia
grafo = pd.DataFrame(index=V, columns=V)
grafo = grafo.fillna(0)  # Rellenar con ceros

# Caminos de los grafos
grafo.loc['Casa', 'Sta Sofia'] = 4
grafo.loc['Casa', 'Copalita'] = 10

grafo.loc['Sta Sofia', 'Guadalajara'] = 7
grafo.loc['Sta Sofia', 'Casa'] = 7

grafo.loc['Copalita', 'Juan Gil Preciado'] = 20
grafo.loc['Copalita', 'Casa'] = 10

grafo.loc['Guadalajara', 'Angel Leano'] = 18
grafo.loc['Guadalajara', 'Sta Sofia'] = 7

grafo.loc['Juan Gil Preciado', 'Angel Leano'] = 23
grafo.loc['Juan Gil Preciado', 'Copalita'] = 20

grafo.loc['Angel Leano', 'La cima'] = 10
grafo.loc['Angel Leano', 'Guadalajara'] = 18

grafo.loc['La cima', 'Valdepenas'] = 17
grafo.loc['La cima', 'Angel Leano'] = 17

grafo.loc['Juan Gil Preciado', 'Arco del triunfo'] = 12
grafo.loc['Juan Gil Preciado', 'Copalita'] = 20

grafo.loc['Arco del triunfo', 'Valdepenas'] = 17
grafo.loc['Arco del triunfo', 'Juan Gil Preciado'] = 17

# Busqueda a la ancho
def busqueda_a_lo_ancho(inicio, objetivo, grafo):
    cola = deque([inicio])
    visitados = {inicio: None}  #Se usa un diccionario
    while cola:
        nodo_actual = cola.popleft()
        
        # Comparación al objetivo
        if nodo_actual == objetivo:
            # Reconstruir el camino desde el objetivo al inicio
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = visitados[nodo_actual]
            return camino[::-1]  # Devolver el camino en orden correcto
        
        # Explorar caminos del nodo actual
        for vecino in grafo.columns:
            if grafo.loc[nodo_actual, vecino] > 0 and vecino not in visitados:
                visitados[vecino] = nodo_actual
                cola.append(vecino)

    return None  # Si no hay camino al objetiv

# Ejecutar la búsqueda desde 'Casa' a 'Valdepenas'
camino = busqueda_a_lo_ancho('Casa', 'Valdepenas', grafo)

print("Camino más corto de Casa a Valdepeñas:", camino)
