from tkinter import messagebox
import webbrowser
import json
import os

# Configuración inicial de CustomTkinter
ctk.set_appearance_mode("dark")  # Apariencia oscura
ctk.set_default_color_theme("dark-blue")  # Tema oscuro

# Ruta al archivo JSON que contiene la base de datos
ARCHIVO_BASE_DATOS = "reglas.json"

# ========================
# SECCIÓN 1: MANEJO DE LA BASE DE DATOS
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

# ========================
# SECCIÓN 2: MOTOR DE INFERENCIA
# ========================
def motor_inferencia(hecho_inicial, reglas):
    """
    Realiza encadenamiento hacia adelante con las reglas dadas.
    """
    hechos = set([hecho_inicial])  # Hechos iniciales
    conclusiones = set()

    while True:
        nueva_conclusion = False
        for regla in reglas:
            # Verificar si todas las condiciones de la regla están en los hechos actuales
            if all(condicion in hechos for condicion in regla["condiciones"]):
                conclusion = regla["conclusion"]
                if conclusion not in conclusiones:
                    conclusiones.add(conclusion)
                    hechos.add(conclusion)
                    nueva_conclusion = True

        if not nueva_conclusion:
            break

    return list(conclusiones)

def procesar_respuesta(seleccion):
    """Procesa la respuesta del usuario y ejecuta el motor de inferencia."""
    reglas = BASE_DATOS["reglas"]
    return motor_inferencia(seleccion, reglas)

# ========================
# SECCIÓN 3: MANEJO DE INTERFAZ
# ========================
def cerrar_aplicacion():
    """Cierra la aplicación de manera segura."""
    ventana_principal.destroy()
    os._exit(0)

def abrir_subventana(categoria, opciones):
    """Abre una subventana para que el usuario seleccione un hecho."""
    ventana_principal.withdraw()  # Oculta la ventana principal
    ventana_secundaria = ctk.CTkToplevel(ventana_principal)
    ventana_secundaria.title(f"Diagnóstico: {categoria}")
    ventana_secundaria.geometry("500x400")
    ventana_secundaria.configure(bg="#1A1A1A")
    ventana_secundaria.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

    # Pregunta principal
    label = ctk.CTkLabel(ventana_secundaria, text=f"Seleccione un hecho de {categoria}:", font=("Calibri Light", 16), text_color="white")
    label.pack(pady=20)

    # Opciones de la categoría
    for opcion in opciones:
        btn = ctk.CTkButton(
            ventana_secundaria,
            text=opcion,
            fg_color="#6A2ECC",
            hover_color="#000077",
            text_color="white",
            command=lambda o=opcion: mostrar_diagnostico(o, ventana_secundaria)
        )
        btn.pack(pady=10)

def mostrar_diagnostico(hecho, ventana_actual):
    """Muestra el diagnóstico basado en el hecho seleccionado y la inferencia realizada."""
    ventana_actual.destroy()  # Cierra la ventana actual
    reglas = BASE_DATOS["reglas"]

    # Procesar la inferencia y obtener la conclusión
    conclusiones = motor_inferencia(hecho, reglas)

    ventana_diagnostico = ctk.CTkToplevel(ventana_principal)
    ventana_diagnostico.title("Diagnóstico Final")
    ventana_diagnostico.geometry("500x600")
    ventana_diagnostico.configure(bg="#1A1A1A")
    ventana_diagnostico.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

    # Título principal
    label_titulo = ctk.CTkLabel(
        ventana_diagnostico,
        text="Diagnóstico Final",
        font=("Calibri Light", 28),
        text_color="white"
    )
    label_titulo.pack(pady=10)

    # Imagen del emoji debajo del título
    try:
        imagen_emoji = Image.open(r"C:\2_Diagnostico de reloj\Imagenes\Emoji.png")
        imagen_emoji_resized = imagen_emoji.resize((150, 150), Image.Resampling.LANCZOS)
        imagen_emoji_tk = ImageTk.PhotoImage(imagen_emoji_resized)
        label_imagen_emoji = ctk.CTkLabel(ventana_diagnostico, image=imagen_emoji_tk, text="")
        label_imagen_emoji.image = imagen_emoji_tk
        label_imagen_emoji.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen del emoji: {e}")

    # Mostrar las conclusiones derivadas
    for conclusion in conclusiones:
        regla_aplicada = next((regla for regla in reglas if regla["conclusion"] == conclusion), None)
        if regla_aplicada:
            diagnostico_label = ctk.CTkLabel(
                ventana_diagnostico,
                text=f"Diagnóstico: {regla_aplicada['conclusion']}",
                font=("Calibri Light", 24),
                text_color="white",
                wraplength=450
            )
            diagnostico_label.pack(pady=20)

            explicacion_label = ctk.CTkLabel(
                ventana_diagnostico,
                text=f"Explicación: {regla_aplicada['explicacion']}",
                font=("Calibri Light", 14),
                text_color="white",
                wraplength=450
            )
            explicacion_label.pack(pady=10)

            if "video" in regla_aplicada and regla_aplicada["video"]:
                try:
                    imagen_icono_youtube = Image.open(r"C:\2_Diagnostico de reloj\Imagenes\Icono youtube.png")
                    imagen_icono_resized = imagen_icono_youtube.resize((30, 30), Image.Resampling.LANCZOS)
                    imagen_icono_tk = ImageTk.PhotoImage(imagen_icono_resized)
                    icono_youtube_label = ctk.CTkLabel(ventana_diagnostico, image=imagen_icono_tk, text="")
                    icono_youtube_label.image = imagen_icono_tk
                    icono_youtube_label.pack(pady=5)

                    def abrir_video(url=regla_aplicada["video"]):
                        webbrowser.open(url)

                    btn_video = ctk.CTkButton(
                        ventana_diagnostico,
                        text="Ver video en YouTube",
                        fg_color="#6A2ECC",
                        hover_color="#000077",
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
        fg_color="#6A2ECC",
        hover_color="#000077",
        text_color="white",
        command=lambda: [ventana_diagnostico.destroy(), ventana_principal.deiconify()]
    )
    btn_inicio.pack(pady=20)

# ========================
# SECCIÓN 4: VENTANA PRINCIPAL
# ========================
ventana_principal = ctk.CTk()
ventana_principal.title("Sistema Experto: Diagnóstico de Relojes de Cuarzo")
ventana_principal.geometry("500x500")
ventana_principal.configure(bg="#1A1A1A")
ventana_principal.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

titulo = ctk.CTkLabel(ventana_principal, text="Diagnóstico de Relojes de Cuarzo", font=("Calibri Light", 24), text_color="white")
titulo.pack(pady=20)

CATEGORIAS = {
    "Precisión": ["El reloj se atrasa", "El reloj se adelanta", "El reloj pierde precisión de forma irregular"],
    "Movimiento": ["El segundero se detiene ocasionalmente", "El segundero avanza de forma errática", "El segundero no avanza pero las otras agujas sí"],
    "Condiciones": ["Se detiene cerca de equipos eléctricos", "El reloj acumula polvo o suciedad", "El reloj se detiene al exponerse al agua"],
    "Falla Física": ["El reloj no responde tras un golpe", "El reloj presenta marcas de humedad", "El reloj tiene componentes sueltos"]
}

for categoria, opciones in CATEGORIAS.items():
    btn = ctk.CTkButton(
        ventana_principal,
        text=f"{categoria}",
        fg_color="#6A2ECC",
        hover_color="#000077",
        text_color="white",
        command=lambda c=categoria, o=opciones: abrir_subventana(c, o)
    )
    btn.pack(pady=10)

ventana_principal.mainloop()
