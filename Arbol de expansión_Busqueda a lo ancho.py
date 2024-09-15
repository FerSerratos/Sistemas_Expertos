import pandas as pd

V = ['Casa', 'Copalita', 'Sta Sofia', 'Guadalajara', 'Juan Gil Preciado', 
     'Angel Leano', 'Valdepenas', 'Arco del triunfo', 'La cima']

# Crear la matriz de adyacencia
grafo = pd.DataFrame(index=V, columns=V)
grafo = grafo.fillna(0)  # Rellenar con ceros

# Caminos de la calle
grafo.loc['Casa', 'Sta Sofia'] = 4
grafo.loc['Casa', 'Copalita'] = 10

grafo.loc['Sta Sofia', 'Guadalajara'] = 7
grafo.loc['Sta Sofia', 'Casa'] = 4

grafo.loc['Copalita', 'Juan Gil Preciado'] = 20
grafo.loc['Copalita', 'Casa'] = 10

grafo.loc['Guadalajara', 'Angel Leano'] = 18
grafo.loc['Guadalajara', 'Sta Sofia'] = 7

grafo.loc['Juan Gil Preciado', 'Angel Leano'] = 23
grafo.loc['Juan Gil Preciado', 'Copalita'] = 20

grafo.loc['Angel Leano', 'La cima'] = 10
grafo.loc['Angel Leano', 'Guadalajara'] = 18

grafo.loc['La cima', 'Valdepenas'] = 17
grafo.loc['La cima', 'Angel Leano'] = 10

grafo.loc['Juan Gil Preciado', 'Arco del triunfo'] = 12
grafo.loc['Juan Gil Preciado', 'Copalita'] = 20

grafo.loc['Arco del triunfo', 'Valdepenas'] = 17
grafo.loc['Arco del triunfo', 'Juan Gil Preciado'] = 12

# Definición del arbol 
def Arbol(V1):
    S = [V1] 
    Vp = [V1]
    Ep = []  
    s = []  
    d = V.copy()  
    d.remove(V1)  

    while True:
        for x in S:
            # Encuentra los vecinos de x que no han sido explorados
            v = [y for y in d if y in grafo.loc[grafo[x] > 0, x]]
            # Agregar aristas y vértices al árbol de expansión
            _ = [(Ep.append((x, y)), Vp.append(y), d.remove(y), s.append(y)) for y in v]

        if not s:
            break
        S = s.copy()
        s = []

    return Ep  # Retornar solo las aristas del árbol

# Iniciamos de la calle de mi trabajo
nodo_inicial = 'Valdepenas'

# Llamamos el arbol de expansión
arbol_expansion = Arbol(nodo_inicial)

# Imprimir el árbol de expansión
print("Árbol de expansión:")
for arista in arbol_expansion:
    print(f"{arista[0]} -- {arista[1]}")

