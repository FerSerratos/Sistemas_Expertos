import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random

# Rutas de las imágenes (ajusta la ruta de la carpeta de acuerdo a tu sistema)
ruta_carpeta = "C:/Users/x/Documents/1_Ingeniería/Sistemas expertos/2do parcial/Clue/"
imagenes = {
    "inicio": ruta_carpeta + "Inicio.jpg",
    "historia": ruta_carpeta + "Historia.jpg",
    "menu": ruta_carpeta + "Menu.jpg",
    "personaje": ruta_carpeta + "Personaje.jpg",
    "lugar": ruta_carpeta + "Lugar.jpg",
    "final": ruta_carpeta + "Final.jpg"
}

# Combinación ganadora (culpable, arma, lugar) seleccionada aleatoriamente
personajes = ["Persona A", "Persona B", "Persona C", "Persona D", "Persona E"]
armas = ["Arma A", "Arma B", "Arma C", "Arma D", "Arma E"]
lugares = ["Lugar A", "Lugar B", "Lugar C", "Lugar D", "Lugar E"]

culpable = random.choice(personajes)
arma_correcta = random.choice(armas)
lugar_correcto = random.choice(lugares)

# Variables para el contador de intentos
intentos_restantes = 5

# Función para cargar y redimensionar imágenes
def cargar_imagen(nombre_imagen, ancho=400, alto=300):
    imagen = Image.open(imagenes[nombre_imagen])
    imagen = imagen.resize((ancho, alto), Image.LANCZOS)  # Cambiamos ANTIALIAS por LANCZOS
    return ImageTk.PhotoImage(imagen)

# Funciones para mostrar ventanas
def mostrar_ventana_inicio():
    ventana_inicio = tk.Toplevel()
    ventana_inicio.title("Inicio")
    ventana_inicio.geometry("400x300")
    img = cargar_imagen("inicio")
    label = tk.Label(ventana_inicio, image=img)
    label.image = img
    label.pack()
    boton_siguiente = tk.Button(ventana_inicio, text="Siguiente", command=lambda: [ventana_inicio.destroy(), mostrar_ventana_historia()])
    boton_siguiente.pack(side="bottom", anchor="se")

def mostrar_ventana_historia():
    ventana_historia = tk.Toplevel()
    ventana_historia.title("Historia")
    ventana_historia.geometry("400x300")
    img = cargar_imagen("historia")
    label = tk.Label(ventana_historia, image=img)
    label.image = img
    label.pack()
    boton_siguiente = tk.Button(ventana_historia, text="Siguiente", command=lambda: [ventana_historia.destroy(), mostrar_ventana_menu()])
    boton_siguiente.pack(side="bottom", anchor="sw")

def mostrar_ventana_menu():
    ventana_menu = tk.Toplevel()
    ventana_menu.title("Menú")
    ventana_menu.geometry("400x300")
    img = cargar_imagen("menu")
    label = tk.Label(ventana_menu, image=img)
    label.image = img
    label.pack()

    boton_personaje = tk.Button(ventana_menu, text="Personaje", command=lambda: [ventana_menu.destroy(), mostrar_ventana_personaje()])
    boton_personaje.pack(side="left", expand=True)

    boton_lugar = tk.Button(ventana_menu, text="Lugar", command=lambda: [ventana_menu.destroy(), mostrar_ventana_lugar()])
    boton_lugar.pack(side="left", expand=True)

    boton_arma = tk.Button(ventana_menu, text="Arma", command=lambda: [ventana_menu.destroy(), mostrar_ventana_arma()])
    boton_arma.pack(side="left", expand=True)

def mostrar_ventana_personaje():
    global intentos_restantes
    if intentos_restantes > 0:
        intentos_restantes -= 1
        ventana_personaje = tk.Toplevel()
        ventana_personaje.title("Selecciona un Personaje")
        ventana_personaje.geometry("400x300")
        img = cargar_imagen("personaje")
        label = tk.Label(ventana_personaje, image=img)
        label.image = img
        label.pack()

        # Crear botones de personajes con descripciones
        for persona in personajes:
            boton = tk.Button(ventana_personaje, text=persona, command=lambda p=persona: mostrar_descripcion(ventana_personaje, p))
            boton.pack()

def mostrar_ventana_arma():
    global intentos_restantes
    if intentos_restantes > 0:
        intentos_restantes -= 1
        ventana_arma = tk.Toplevel()
        ventana_arma.title("Selecciona un Arma")
        ventana_arma.geometry("400x300")
        img = cargar_imagen("lugar")  # Cambia a la imagen de armas si la tienes
        label = tk.Label(ventana_arma, image=img)
        label.image = img
        label.pack()

        # Crear botones de armas con descripciones
        for arma in armas:
            boton = tk.Button(ventana_arma, text=arma, command=lambda a=arma: mostrar_descripcion(ventana_arma, a))
            boton.pack()

def mostrar_ventana_lugar():
    global intentos_restantes
    if intentos_restantes > 0:
        intentos_restantes -= 1
        ventana_lugar = tk.Toplevel()
        ventana_lugar.title("Selecciona un Lugar")
        ventana_lugar.geometry("400x300")
        img = cargar_imagen("lugar")
        label = tk.Label(ventana_lugar, image=img)
        label.image = img
        label.pack()

        # Crear botones de lugares con descripciones
        for lugar in lugares:
            boton = tk.Button(ventana_lugar, text=lugar, command=lambda l=lugar: mostrar_descripcion(ventana_lugar, l))
            boton.pack()

    # Si no quedan intentos, abrir ventana final
    if intentos_restantes == 0:
        mostrar_ventana_final()

def mostrar_descripcion(ventana_anterior, opcion):
    ventana_anterior.destroy()
    ventana_emergente = tk.Toplevel()
    ventana_emergente.geometry("250x150")
    descripcion = f"Descripción de {opcion}"  # Aquí podrías poner descripciones detalladas si quieres
    tk.Label(ventana_emergente, text=descripcion).pack()
    tk.Button(ventana_emergente, text="Cerrar", command=ventana_emergente.destroy).pack()

def mostrar_ventana_final():
    ventana_final = tk.Toplevel()
    ventana_final.title("¿Quién es el culpable?")
    ventana_final.geometry("400x300")
    img = cargar_imagen("final")
    label = tk.Label(ventana_final, image=img)
    label.image = img
    label.pack()

    for persona in personajes:
        boton = tk.Button(ventana_final, text=persona, command=lambda p=persona: verificar_culpable(p))
        boton.pack()

def verificar_culpable(eleccion):
    if eleccion == culpable:
        messagebox.showinfo("Resultado", "¡Correcto! Has encontrado al culpable.")
    else:
        messagebox.showinfo("Resultado", "Incorrecto. No era el culpable.")

# Ventana principal
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal
mostrar_ventana_inicio()
root.mainloop()
