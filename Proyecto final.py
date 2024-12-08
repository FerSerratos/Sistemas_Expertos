# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 14:12:00 2024

@author: x
"""

import customtkinter as ctk  # Importa CustomTkinter
from PIL import Image, ImageTk  # Importa Pillow para trabajar con imágenes
from tkinter import messagebox
import webbrowser
import json
import os

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("dark")  # Apariencia oscura
ctk.set_default_color_theme("dark-blue")  # Tema oscuro

# Archivo JSON que contiene la base de datos
ARCHIVO_BASE_DATOS = "base_datos.json"

# ========================
# SECCIÓN 1: CARGA Y GUARDA DE BASE DE DATOS
# ========================
def cargar_base_datos():
    """Carga la base de datos desde un archivo JSON."""
    if os.path.exists(ARCHIVO_BASE_DATOS):
        with open(ARCHIVO_BASE_DATOS, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    else:
        messagebox.showerror("Error", f"No se encontró el archivo {ARCHIVO_BASE_DATOS}.")
        return None

# Cargar la base de datos
BASE_DATOS = cargar_base_datos()

if not BASE_DATOS:
    raise FileNotFoundError(f"No se pudo cargar el archivo {ARCHIVO_BASE_DATOS}.")

# ============================
# SECCIÓN 2: MOTOR DE INFERENCIA
# ============================
def obtener_pregunta(categoria):
    """Obtiene la pregunta inicial para una categoría."""
    return BASE_DATOS["sintomas_generales"][categoria]["pregunta"]

def obtener_opciones(categoria):
    """Obtiene las opciones disponibles para una categoría."""
    return BASE_DATOS["sintomas_generales"][categoria]["opciones"]

def procesar_respuesta(categoria, seleccion):
    """Procesa la respuesta del usuario y devuelve el diagnóstico, la explicación, la solución y el enlace."""
    opciones = obtener_opciones(categoria)
    if seleccion in opciones:
        return (
            opciones[seleccion]["diagnostico"],
            opciones[seleccion]["explicacion"],
            opciones[seleccion]["solucion"],
            opciones[seleccion]["video"]
        )
    return (
        "Diagnóstico desconocido",
        "No hay explicación disponible.",
        "No hay solución disponible.",
        None
    )

# ============================
# SECCIÓN 3: FUNCIONES DE INTERFAZ
# ============================
def abrir_ventana(categoria):
    """Abre una ventana para una categoría específica."""
    ventana_principal.withdraw()  # Oculta la ventana principal
    ventana_secundaria = ctk.CTkToplevel(ventana_principal)
    ventana_secundaria.title("Diagnóstico del Reloj")
    ventana_secundaria.geometry("500x400")
    ventana_secundaria.configure(bg="#1A1A1A")  # Fondo negro

    pregunta = obtener_pregunta(categoria)
    opciones = obtener_opciones(categoria)

    label = ctk.CTkLabel(ventana_secundaria, text=pregunta, font=("Calibri Light", 16), text_color="white")
    label.pack(pady=20)

    for opcion in opciones.keys():
        btn = ctk.CTkButton(
            ventana_secundaria,
            text=opcion,
            fg_color="#6A2ECC",  # Morado oscuro
            hover_color="#000077",  # Azul oscuro al pasar el cursor
            text_color="white",
            command=lambda o=opcion: mostrar_diagnostico(categoria, o, ventana_secundaria)
        )
        btn.pack(pady=10)

def mostrar_diagnostico(categoria, seleccion, ventana_actual):
    """Muestra el diagnóstico, explicación, solución y enlace al video."""
    ventana_actual.destroy()  # Cierra la ventana actual
    diagnostico, explicacion, solucion, video = procesar_respuesta(categoria, seleccion)

    ventana_diagnostico = ctk.CTkToplevel(ventana_principal)
    ventana_diagnostico.title("Diagnóstico Final")
    ventana_diagnostico.geometry("500x600")
    ventana_diagnostico.configure(bg="#1A1A1A")  # Fondo negro

    # Título principal
    label_titulo = ctk.CTkLabel(
        ventana_diagnostico,
        text="Diagnóstico Final",
        font=("Calibri Light", 28),  # Aumentar tamaño de letra
        text_color="white"
    )
    label_titulo.pack(pady=10)

    # Imagen del emoji debajo del título
    try:
        imagen_emoji = Image.open(r"C:\2_Diagnostico de reloj\Imagenes\Emoji.png")
        imagen_emoji_resized = imagen_emoji.resize((150, 150), Image.Resampling.LANCZOS)  # Escalar a la mitad
        imagen_emoji_tk = ImageTk.PhotoImage(imagen_emoji_resized)
        label_imagen_emoji = ctk.CTkLabel(ventana_diagnostico, image=imagen_emoji_tk, text="")
        label_imagen_emoji.image = imagen_emoji_tk  # Evitar que se recoja por el garbage collector
        label_imagen_emoji.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen del emoji: {e}")

    # Diagnóstico en letra grande
    diagnostico_label = ctk.CTkLabel(
        ventana_diagnostico,
        text=f"{diagnostico}",
        font=("Calibri Light", 24),  # Tamaño grande
        text_color="white",
        wraplength=450
    )
    diagnostico_label.pack(pady=20)

    # Explicación y solución
    explicacion_label = ctk.CTkLabel(
        ventana_diagnostico,
        text=f"Explicación: {explicacion}",
        font=("Calibri Light", 14),
        text_color="white",
        wraplength=450
    )
    explicacion_label.pack(pady=10)

    solucion_label = ctk.CTkLabel(
        ventana_diagnostico,
        text=f"Solución: {solucion}",
        font=("Calibri Light", 14),
        text_color="white",
        wraplength=450
    )
    solucion_label.pack(pady=10)

    # Botón de video con ícono de YouTube
    if video:
        try:
            imagen_icono_youtube = Image.open(r"C:\2_Diagnostico de reloj\Imagenes\Icono youtube.png")
            imagen_icono_resized = imagen_icono_youtube.resize((30, 30), Image.Resampling.LANCZOS)
            imagen_icono_tk = ImageTk.PhotoImage(imagen_icono_resized)

            icono_youtube_label = ctk.CTkLabel(ventana_diagnostico, image=imagen_icono_tk, text="")
            icono_youtube_label.image = imagen_icono_tk  # Evitar que se recoja por el garbage collector
            icono_youtube_label.pack(pady=5)

            def abrir_video():
                webbrowser.open(video)

            btn_video = ctk.CTkButton(
                ventana_diagnostico,
                text="Ver video en YouTube",
                fg_color="#6A2ECC",  # Morado oscuro
                hover_color="#000077",  # Azul oscuro
                text_color="white",
                command=abrir_video
            )
            btn_video.pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el ícono de YouTube: {e}")

    # Botón para regresar al inicio
    btn_inicio = ctk.CTkButton(
        ventana_diagnostico,
        text="Regresar al inicio",
        fg_color="#6A2ECC",  # Morado oscuro
        hover_color="#000077",  # Azul oscuro
        text_color="white",
        command=lambda: [ventana_diagnostico.destroy(), ventana_principal.deiconify()]
    )
    btn_inicio.pack(pady=20)



# =============================
# SECCIÓN 4: VENTANA PRINCIPAL
# =============================
ventana_principal = ctk.CTk()
ventana_principal.title("Sistema Experto: Diagnóstico de Relojes de Cuarzo")
ventana_principal.geometry("500x500")
ventana_principal.configure(bg="#1A1A1A")  # Fondo negro

titulo = ctk.CTkLabel(ventana_principal, text="Diagnóstico de Relojes de Cuarzo", font=("Calibri Light", 24), text_color="white")
titulo.pack(pady=20)

label = ctk.CTkLabel(ventana_principal, text="Selecciona un síntoma general para comenzar:", font=("Calibri Light", 16), text_color="white")
label.pack(pady=10)

for categoria in BASE_DATOS["sintomas_generales"]:
    btn = ctk.CTkButton(
        ventana_principal,
        text=f"Problemas de {categoria}",
        fg_color="#6A2ECC",  # Morado oscuro
        hover_color="#000077",  # Azul oscuro
        text_color="white",
        command=lambda c=categoria: abrir_ventana(c)
    )
    btn.pack(pady=10)

# Agregar la imagen debajo de los botones
imagen_ruta = r"C:\2_Diagnostico de reloj\Imagenes\Agujas de reloj.png"

try:
    imagen = Image.open(imagen_ruta)
    imagen_resized = imagen.resize((300, 300), Image.Resampling.LANCZOS)  # Escala la imagen
    imagen_tk = ImageTk.PhotoImage(imagen_resized)

    label_imagen = ctk.CTkLabel(ventana_principal, image=imagen_tk, text="")
    label_imagen.pack(pady=20)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")

# Inicia el loop principal de la aplicación
ventana_principal.mainloop()
