# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pandas as pd
import re
from openpyxl import load_workbook
import os

# Ruta de la carpeta de imágenes
ruta_imagenes = r"C:\Users\x\Documents\1_Ingeniería\Sistemas expertos\2do parcial\Adivina quien\Ventanas"

# Diccionario de imágenes con las rutas absolutas
imagenes = {
    "inicio": os.path.join(ruta_imagenes, "inicio.jpg"),
    "arruga": os.path.join(ruta_imagenes, "arruga.jpg"),
    "elastica": os.path.join(ruta_imagenes, "elastica.jpg"),
    "fluida": os.path.join(ruta_imagenes, "fluida.jpg"),
    "transpirable": os.path.join(ruta_imagenes, "transpirable.jpg"),
    "natural": os.path.join(ruta_imagenes, "natural.jpg"),
    "respuesta": os.path.join(ruta_imagenes, "respuesta.jpg"),
    "sin_respuesta": os.path.join(ruta_imagenes, "sin respuesta.jpg"),
    "nueva_pregunta": os.path.join(ruta_imagenes, "nueva pregunta.jpg")
}

# Ruta del archivo Excel
file_path = 'Propiedades_textiles.xlsx'

# Cargar el archivo Excel y normalizar los nombres de las columnas y valores a minúsculas y sin acentos
df_telas = pd.read_excel(file_path)
df_telas.columns = [re.sub(r'[^\w\s]', '', col.lower()).replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') for col in df_telas.columns]
df_telas = df_telas.applymap(lambda x: re.sub(r'[^\w\s]', '', x.lower()).replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u') if isinstance(x, str) else x)

# Lista completa de preguntas para cada característica (también normalizadas)
preguntas = {
    "natural": "¿Es la tela natural?",
    "elastica": "¿Es la tela elástica?",
    "arruga": "¿Es propensa a arrugarse?",
    "transpirable": "¿Es transpirable?",
    "fluida": "¿Es fluida al caer?",
    "gruesa": "¿Es una tela gruesa?",
    "rugosa": "¿Tiene una textura rugosa?",
    "brilla": "¿La tela brilla?"
}

class TelaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivina la Tela")
        self.current_image = None
        self.posibles_telas = df_telas.copy()
        self.respuestas = {}

        # Inicializar en la ventana de inicio
        self.show_inicio()

    def show_image(self, path):
        image = Image.open(path)
        
        # Escalar la imagen a la mitad de su tamaño original
        width, height = image.size
        new_width = width // 2
        new_height = height // 2
        image = image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convertir la imagen escalada en un objeto compatible con Tkinter
        self.current_image = ImageTk.PhotoImage(image)
        
        # Ajustar la ventana al tamaño de la imagen escalada
        self.root.geometry(f"{new_width}x{new_height}")
        
        # Mostrar la imagen en el fondo
        bg_label = tk.Label(self.root, image=self.current_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def show_inicio(self):
        self.clear_window()
        self.show_image(imagenes["inicio"])
    
        # Botón de iniciar, con estilo modificado
        iniciar_btn = tk.Button(
            self.root,
            text="Iniciar",
            command=self.show_pregunta_natural,
            width=15,
            height=2,
            font=("Arial", 16, "normal"),
            bg="white",
            fg="black",
            relief="flat"
        )
        iniciar_btn.place(x=190, y=450)
    
        # Botón de cerrar, con estilo modificado
        cerrar_btn = tk.Button(
            self.root,
            text="Cerrar",
            command=self.root.destroy,
            width=15,
            height=2,
            font=("Arial", 16, "normal"),
            bg="white",
            fg="black",
            relief="flat"
        )
        cerrar_btn.place(x=450, y=450)


    def show_pregunta_natural(self):
        self.show_pregunta("natural", self.show_pregunta_elastica)

    def show_pregunta_elastica(self):
        self.show_pregunta("elastica", self.show_pregunta_fluida)

    def show_pregunta_fluida(self):
        self.show_pregunta("fluida", self.show_pregunta_transpirable)

    def show_pregunta_transpirable(self):
        self.show_pregunta("transpirable", self.show_pregunta_arruga)

    def show_pregunta_arruga(self):
        self.show_pregunta("arruga", self.show_resultado)

    def show_pregunta(self, atributo, next_callback):
        self.clear_window()
        self.show_image(imagenes[atributo])

        # Estilo y posición de botones
        btn_style = {
            "width": 15,
            "height": 2,
            "font": ("Arial", 16, "normal"),
            "bg": "white",
            "fg": "black",
            "relief": "flat"
        }
        
        # Posiciones específicas para los botones en cada ventana
        posiciones = {
            "natural": {"si": (550, 375), "no": (750, 375)},
            "elastica": {"si": (500, 250), "no": (700, 250)},
            "fluida": {"si": (550, 150), "no": (750, 150)},         # Aseguramos posiciones para "fluida"
            "transpirable": {"si": (550, 400), "no": (750, 400)},
            "arruga": {"si": (550, 400), "no": (750, 400)}
        }

        # Verificar que el atributo tenga una posición definida, en caso de agregar nuevos atributos en el futuro
        if atributo not in posiciones:
            posiciones[atributo] = {"si": (550, 400), "no": (750, 400)}  # Posición por defecto si falta en `posiciones`

        # Crear botones con estilos y posiciones específicas para cada atributo
        si_btn = tk.Button(
            self.root,
            text="Sí",
            command=lambda: self.procesar_respuesta(atributo, "si", next_callback),
            **btn_style
        )
        si_btn.place(x=posiciones[atributo]["si"][0], y=posiciones[atributo]["si"][1])

        no_btn = tk.Button(
            self.root,
            text="No",
            command=lambda: self.procesar_respuesta(atributo, "no", next_callback),
            **btn_style
        )
        no_btn.place(x=posiciones[atributo]["no"][0], y=posiciones[atributo]["no"][1])

    def procesar_respuesta(self, atributo, respuesta, next_callback):
        self.respuestas[atributo] = respuesta
        if atributo in self.posibles_telas.columns:
            self.posibles_telas = self.posibles_telas[self.posibles_telas[atributo] == respuesta]
        
        if self.posibles_telas.empty:
            self.show_sin_respuesta()
        elif len(self.posibles_telas) == 1:
            self.show_resultado(self.posibles_telas.iloc[0]['tela'])
        else:
            next_callback()

    def show_resultado(self, tela=None):
        self.clear_window()
        self.show_image(imagenes["respuesta"])
        
        # Mostrar tela encontrada o mensaje de error
        if tela:
            mensaje = f"{tela}"
        else:
            mensaje = "No se encontró :("
        
        respuesta_label = tk.Label(self.root, text=mensaje, font=("Arial", 24), bg="#E8E3CF", fg="black")

        respuesta_label.place(x=300, y=140)

        # Botones de regresar e ingresar otra respuesta
        inicio_btn = tk.Button(self.root, text="Regresar al inicio", command=self.show_inicio, width=20)
        inicio_btn.place(x=120, y=220)

        otra_btn = tk.Button(self.root, text="Escribir otra respuesta", command=self.show_sin_respuesta, width=20)
        otra_btn.place(x=500, y=220)

    def show_sin_respuesta(self):
        self.clear_window()
        self.show_image(imagenes["sin_respuesta"])
    
        # Cuadro de texto para ingresar el nombre de la nueva tela sin la opción de característica
        nombre_label = tk.Label(self.root, text="Nombre de la tela:", font=("Arial", 14))
        nombre_label.place(x=30, y=320)
        nombre_entry = tk.Entry(self.root, width=30, font=("Arial", 14))
        nombre_entry.place(x=200, y=320)
    
        guardar_btn = tk.Button(self.root, text="Guardar", width=10, command=lambda: self.guardar_nueva_tela(nombre_entry.get()))
        guardar_btn.place(x=350, y=450)
    
    def guardar_nueva_tela(self, nombre):
        if nombre:
            # Aquí guardaríamos los datos en el archivo Excel
            nueva_entrada = {**self.respuestas, "tela": nombre}
            nueva_entrada.update({col: "no" for col in df_telas.columns if col not in nueva_entrada})
            df_telas.loc[len(df_telas)] = nueva_entrada
    
            with pd.ExcelWriter(file_path, engine="openpyxl", mode="w") as writer:
                df_telas.to_excel(writer, index=False)
    
            messagebox.showinfo("Guardado", f"Tela '{nombre}' guardada.")
            self.show_inicio()
        else:
            messagebox.showwarning("Advertencia", "Por favor completa el campo del nombre de la tela.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Ejecutar la aplicación
root = tk.Tk()
app = TelaApp(root)
root.mainloop()

