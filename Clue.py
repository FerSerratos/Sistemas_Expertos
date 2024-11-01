# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import random
import os

# Ruta de las imágenes (ajusta a tu ruta)
ruta_carpeta = "C:/Users/x/Documents/1_Ingeniería/Sistemas expertos/2do parcial/Clue/"

class ClueGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Clue")
        self.intentos = 0  # Contador de intentos
        self.max_intentos = 3

        # Combinaciones correctas con descripciones sospechosas
        self.combinaciones_correctas = [
            {
                "personaje": "Martin Teórico",
                "lugar": "Estación de Servicio Abandonada",
                "arma": "Corta-cables",
                "descripcion": "Se vio al conspiracionista en la estación de servicio con una herramienta sospechosa en la mano."
            },
            {
                "personaje": "Lucía Santini",
                "lugar": "Parada de Autobús Desierta",
                "arma": "Veneno",
                "descripcion": "Lucía fue vista en la parada de autobús con un frasco de veneno escondido en su bolso."
            },
            {
                "personaje": "Dr. Klaus Stein",
                "lugar": "Entrada a la Central Nuclear",
                "arma": "Láser para cegar al conductor",
                "descripcion": "El Dr. Klaus Stein merodeaba la entrada de la central con un dispositivo láser en su bolsillo."
            },
            {
                "personaje": "Vera Tempus",
                "lugar": "Antiguo Almacén de Mantenimiento",
                "arma": "Arma de diferente tiempo",
                "descripcion": "Vera Tempus estaba en el almacén con un arma que parecía de otra época."
            },
            {
                "personaje": "Elias Von Richman",
                "lugar": "Café Rústico del Pueblo",
                "arma": "Balde con agua",
                "descripcion": "Elias fue visto en el café rústico con un balde de agua que planeaba usar de manera sospechosa."
            }
        ]
        # Historias de relleno (no concluyentes y sin repetir combinaciones)
        self.historias_relleno = [
            {"personaje": "Martin Teórico", "lugar": "Parada de Autobús Desierta", "arma": "Balde con agua", 
             "descripcion": "Martin fue visto esperando en la parada de autobús con un balde, sin nada sospechoso."},
            {"personaje": "Lucía Santini", "lugar": "Estación de Servicio Abandonada", "arma": "Corta-cables", 
             "descripcion": "Lucía estaba en la estación revisando su auto con una herramienta en mano."},
            {"personaje": "Dr. Klaus Stein", "lugar": "Café Rústico del Pueblo", "arma": "Veneno", 
             "descripcion": "Dr. Klaus Stein leía un libro en el café rústico mientras bebía su té."},
            {"personaje": "Vera Tempus", "lugar": "Entrada a la Central Nuclear", "arma": "Láser para cegar al conductor", 
             "descripcion": "Vera esperaba en la entrada de la central observando el horizonte."},
            {"personaje": "Elias Von Richman", "lugar": "Antiguo Almacén de Mantenimiento", "arma": "Arma de diferente tiempo", 
             "descripcion": "Elias revisaba viejas herramientas en el almacén sin ningún propósito aparente."},
            {"personaje": "Martin Teórico", "lugar": "Café Rústico del Pueblo", "arma": "Láser para cegar al conductor", 
             "descripcion": "Martin estaba en el café, probando su nuevo dispositivo láser en un ambiente seguro."},
            {"personaje": "Lucía Santini", "lugar": "Antiguo Almacén de Mantenimiento", "arma": "Arma de diferente tiempo", 
             "descripcion": "Lucía exploraba el viejo almacén, intrigada por los objetos antiguos."},
            {"personaje": "Dr. Klaus Stein", "lugar": "Parada de Autobús Desierta", "arma": "Balde con agua", 
             "descripcion": "El Dr. Klaus Stein fue visto en la parada de autobús cargando un balde de agua."},
            {"personaje": "Vera Tempus", "lugar": "Estación de Servicio Abandonada", "arma": "Corta-cables", 
             "descripcion": "Vera estaba en la estación, ajustando su auto con herramientas básicas."},
            {"personaje": "Elias Von Richman", "lugar": "Entrada a la Central Nuclear", "arma": "Veneno", 
             "descripcion": "Elias discutía sobre química en la entrada de la central sin intención peligrosa."},
            {"personaje": "Martin Teórico", "lugar": "Antiguo Almacén de Mantenimiento", "arma": "Arma de diferente tiempo", 
             "descripcion": "Martin investigaba el almacén buscando pistas de viajes en el tiempo."},
            {"personaje": "Lucía Santini", "lugar": "Entrada a la Central Nuclear", "arma": "Láser para cegar al conductor", 
             "descripcion": "Lucía pasaba por la entrada de la central con un puntero láser para sus clases."},
            {"personaje": "Dr. Klaus Stein", "lugar": "Estación de Servicio Abandonada", "arma": "Corta-cables", 
             "descripcion": "El Dr. Klaus revisaba su auto en la estación de servicio sin urgencia."},
            {"personaje": "Vera Tempus", "lugar": "Café Rústico del Pueblo", "arma": "Veneno", 
             "descripcion": "Vera tomaba un café mientras hablaba sobre hierbas medicinales."},
            {"personaje": "Elias Von Richman", "lugar": "Parada de Autobús Desierta", "arma": "Balde con agua", 
             "descripcion": "Elias fue visto esperando el autobús con un balde lleno de herramientas."},
            {"personaje": "Martin Teórico", "lugar": "Entrada a la Central Nuclear", "arma": "Veneno", 
             "descripcion": "Martin esperaba fuera de la central nuclear, conversando sobre química."},
            {"personaje": "Lucía Santini", "lugar": "Café Rústico del Pueblo", "arma": "Balde con agua", 
             "descripcion": "Lucía estaba en el café con un balde que parecía estar lleno de agua para las plantas."},
            {"personaje": "Dr. Klaus Stein", "lugar": "Antiguo Almacén de Mantenimiento", "arma": "Arma de diferente tiempo", 
             "descripcion": "Dr. Klaus observaba las reliquias del almacén sin mucho interés."},
            {"personaje": "Vera Tempus", "lugar": "Parada de Autobús Desierta", "arma": "Láser para cegar al conductor", 
             "descripcion": "Vera estaba en la parada de autobús mostrando su dispositivo láser como parte de un experimento."},
            {"personaje": "Elias Von Richman", "lugar": "Estación de Servicio Abandonada", "arma": "Corta-cables", 
             "descripcion": "Elias fue visto arreglando su propio auto en la estación de servicio."}
        ]
        

        # Selecciona una combinación ganadora al inicio
        self.configurar_partida()

        # Cargar y redimensionar imágenes
        self.load_images()

        # Mostrar la pantalla de inicio
        self.mostrar_pantalla_inicio()
        
    # Modificar la función `configurar_partida`
    # Modificar la función `configurar_partida`
    # Modificar la función `configurar_partida`
    def configurar_partida(self):
        """Configura una nueva partida con una combinación correcta y cuatro historias de relleno."""
        # Elegir la combinación ganadora
        self.combinacion_ganadora = random.choice(self.combinaciones_correctas)
    
        # Seleccionar historias de relleno sin duplicar personajes, lugares o armas
        personajes_relleno = {self.combinacion_ganadora["personaje"]}
        lugares_relleno = {self.combinacion_ganadora["lugar"]}
        armas_relleno = {self.combinacion_ganadora["arma"]}
        combinaciones_relleno = []
    
        for historia in random.sample(self.historias_relleno, len(self.historias_relleno)):
            if (historia["personaje"] not in personajes_relleno and
                historia["lugar"] not in lugares_relleno and
                historia["arma"] not in armas_relleno):
                combinaciones_relleno.append(historia)
                personajes_relleno.add(historia["personaje"])
                lugares_relleno.add(historia["lugar"])
                armas_relleno.add(historia["arma"])
            if len(combinaciones_relleno) == 4:
                break
    
        # Crear la lista de historias para la partida con la combinación ganadora
        self.historias_partida = [self.combinacion_ganadora] + combinaciones_relleno
    
        # Definir opciones fijas para cada categoría
        self.opciones_personajes = ["Martin Teórico", "Lucía Santini", "Dr. Klaus Stein", "Vera Tempus", "Elias Von Richman"]
        self.opciones_lugares = ["Estación de Servicio Abandonada", "Parada de Autobús Desierta", "Entrada a la Central Nuclear", "Antiguo Almacén de Mantenimiento", "Café Rústico del Pueblo"]
        self.opciones_armas = ["Balde con agua", "Veneno", "Arma de diferente tiempo", "Láser para cegar al conductor", "Corta-cables"]
    
    # Modificar la función `mostrar_pantalla_pistas`
    def mostrar_pantalla_pistas(self, imagen, tipo):
        """Mostrar cinco opciones de pistas con mensaje específico para la combinación."""
        if self.intentos >= self.max_intentos:
            self.mostrar_adivinanza_final()
            return
    
        self.clear_window()
        label = tk.Label(self.root, image=imagen)
        label.pack()
    
        # Escoger opciones fijas según el tipo de pista
        if tipo == "Personaje":
            opciones = self.opciones_personajes
        elif tipo == "Lugar":
            opciones = self.opciones_lugares
        elif tipo == "Arma":
            opciones = self.opciones_armas
    
        # Crear los botones de pistas con descripciones basadas en la historia generada
        y_pos = 200
        for nombre in opciones:
            # Encontrar la historia que corresponde al nombre y tipo actual
            descripcion = next((h["descripcion"] for h in self.historias_partida if h[tipo.lower()] == nombre), "Descripción no disponible")
            tk.Button(self.root, text=nombre,
                      command=lambda desc=descripcion: self.mostrar_pista(desc)).place(x=10, y=y_pos)
            y_pos += 50  # Ajusta el espaciado entre los botones





    def load_images(self):
        """Carga las imágenes necesarias y las redimensiona al 50% del tamaño original."""
        self.inicio_img = self.resize_image("Inicio.jpg")
        self.historia_img = self.resize_image("Historia.jpg")
        self.menu_img = self.resize_image("Menu.jpg")
        self.personaje_img = self.resize_image("Personaje.jpg")
        self.lugar_img = self.resize_image("Lugar.jpg")
        self.arma_img = self.resize_image("Arma.jpg")
        self.final_img = self.resize_image("Final.jpg")

    def resize_image(self, filename):
        """Redimensionar la imagen al 50% del tamaño original."""
        path = os.path.join(ruta_carpeta, filename)
        img = Image.open(path)
        img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
        return ImageTk.PhotoImage(img)


    def mostrar_pantalla_inicio(self):
        """Mostrar la pantalla inicial con estilo de máquina de escribir."""
        self.clear_window()
    
        # Fondo gris oscuro para la ventana principal
        self.root.configure(bg="#333333")
    
        # Crear una etiqueta para la imagen de inicio
        label = tk.Label(self.root, image=self.inicio_img, bg="#333333")
        label.pack()
    
        # Crear el botón con estilo de máquina de escribir
        boton_siguiente = tk.Button(
            self.root, 
            text="Siguiente", 
            command=self.mostrar_pantalla_historia,
            font=("Courier", 14, "bold"),  # Estilo de letra tipo máquina de escribir
            fg="white",  # Color de texto blanco
            bg="#444444",  # Fondo gris oscuro del botón
            activebackground="#555555",  # Fondo gris un poco más claro al hacer clic
            activeforeground="white"  # Color del texto al hacer clic
        )
        
        # Colocar el botón en la posición deseada
        boton_siguiente.place(x=880, y=520)  # Ajusta la posición según sea necesario



    def mostrar_pantalla_historia(self):
        """Mostrar la pantalla de historia introductoria con estilo de máquina de escribir."""
        self.clear_window()
    
        # Fondo gris oscuro para la ventana principal
        self.root.configure(bg="#333333")
    
        # Crear una etiqueta para la imagen de historia
        label = tk.Label(self.root, image=self.historia_img, bg="#333333")
        label.pack()
    
        # Crear el botón con estilo de máquina de escribir
        boton_siguiente = tk.Button(
            self.root, 
            text="Siguiente", 
            command=self.mostrar_menu_opciones,
            font=("Courier", 14, "bold"),  # Estilo de letra tipo máquina de escribir
            fg="white",  # Color de texto blanco
            bg="#444444",  # Fondo gris oscuro del botón
            activebackground="#555555",  # Fondo gris un poco más claro al hacer clic
            activeforeground="white"  # Color del texto al hacer clic
        )
        
        # Colocar el botón en la posición deseada
        boton_siguiente.place(x=880, y=520)  # Ajusta la posición según sea necesario


    def mostrar_menu_opciones(self):
        """Mostrar el menú principal con opciones de pistas, en estilo máquina de escribir."""
        self.clear_window()
    
        # Fondo beige para la ventana principal
        self.root.configure(bg="#F5F5DC")
    
        # Crear una etiqueta para la imagen del menú con fondo beige
        label = tk.Label(self.root, image=self.menu_img, bg="#F5F5DC")
        label.pack()
    
        # Crear botones para las opciones de pistas con estilo de máquina de escribir
        boton_personaje = tk.Button(
            self.root,
            text="Personaje",
            command=self.mostrar_personaje_pistas,
            font=("Courier", 14, "bold"),
            fg="black",  # Letra en negro para buen contraste
            bg="#D2B48C",  # Fondo beige oscuro para los botones
            activebackground="#C0A080",  # Fondo un poco más oscuro al hacer clic
            activeforeground="black"
        )
        boton_personaje.place(x=250, y=200)  # Ajusta la posición según sea necesario
    
        boton_lugar = tk.Button(
            self.root,
            text="Lugar",
            command=self.mostrar_lugar_pistas,
            font=("Courier", 14, "bold"),
            fg="black",
            bg="#D2B48C",
            activebackground="#C0A080",
            activeforeground="black"
        )
        boton_lugar.place(x=450, y=200)  # Ajusta la posición según sea necesario
    
        boton_arma = tk.Button(
            self.root,
            text="Arma",
            command=self.mostrar_arma_pistas,
            font=("Courier", 14, "bold"),
            fg="black",
            bg="#D2B48C",
            activebackground="#C0A080",
            activeforeground="black"
        )
        boton_arma.place(x=650, y=200)  # Ajusta la posición según sea necesario
    
            


    def mostrar_personaje_pistas(self):
        """Mostrar opciones de personajes."""
        self.mostrar_pantalla_pistas(self.personaje_img, "Personaje")

    def mostrar_lugar_pistas(self):
        """Mostrar opciones de lugares."""
        self.mostrar_pantalla_pistas(self.lugar_img, "Lugar")

    def mostrar_arma_pistas(self):
        """Mostrar opciones de armas."""
        self.mostrar_pantalla_pistas(self.arma_img, "Arma")

    def mostrar_pantalla_pistas(self, imagen, tipo):
        """Mostrar cinco opciones de pistas con mensaje específico para la combinación."""
        if self.intentos >= self.max_intentos:
            self.mostrar_adivinanza_final()
            return

        self.clear_window()
        label = tk.Label(self.root, image=imagen)
        label.pack()

        # Crear los botones de pistas (ajusta x, y y el espaciado vertical)
        y_pos = 200
        for combinacion in self.historias_partida:
            tk.Button(self.root, text=combinacion[tipo.lower()],
                      command=lambda desc=combinacion["descripcion"]: self.mostrar_pista(desc)).place(x=10, y=y_pos)
            y_pos += 50  # Ajusta el espaciado entre los botones

    def mostrar_pista(self, descripcion):
        """Mostrar la pista seleccionada y aumentar el contador de intentos."""
        self.intentos += 1
        messagebox.showinfo("Pista", descripcion)
        
        # Volver al menú de opciones o mostrar la adivinanza final
        if self.intentos < self.max_intentos:
            self.mostrar_menu_opciones()
        else:
            self.mostrar_adivinanza_final()

    def mostrar_adivinanza_final(self):
        """Pantalla para adivinar la combinación final."""
        self.clear_window()
        tk.Label(self.root, image=self.final_img).pack()
        tk.Label(self.root, text="¿Quién es el culpable?").place(x=408, y=200)  # Ajusta la posición de la etiqueta

        # ComboBoxes para realizar la adivinanza (ajusta las posiciones x, y de cada ComboBox)
        opciones = [combinacion["personaje"] for combinacion in self.historias_partida]
        self.combo_personaje = self.crear_combobox(opciones, x=355, y=250)
        opciones = [combinacion["lugar"] for combinacion in self.historias_partida]
        self.combo_lugar = self.crear_combobox(opciones, x=355, y=300)
        opciones = [combinacion["arma"] for combinacion in self.historias_partida]
        self.combo_arma = self.crear_combobox(opciones, x=355, y=350)

        # Botón de confirmación de adivinanza (ajusta la posición)
        tk.Button(self.root, text="Confirmar", command=self.comprobar_adivinanza).place(x=450, y=430)

    def crear_combobox(self, opciones, x, y):
        """Crear y devolver un ComboBox en una posición específica, sin selección inicial."""
        combobox = ttk.Combobox(self.root, values=opciones, state="readonly", width=35)  # Ajusta el ancho aquí
        combobox.set("")  # Deja el ComboBox en blanco al inicio
        combobox.place(x=x, y=y)
        return combobox


    def comprobar_adivinanza(self):
        """Verificar si la adivinanza es correcta."""
        personaje = self.combo_personaje.get()
        lugar = self.combo_lugar.get()
        arma = self.combo_arma.get()

        if (personaje == self.combinacion_ganadora["personaje"] and
            lugar == self.combinacion_ganadora["lugar"] and
            arma == self.combinacion_ganadora["arma"]):
            messagebox.showinfo("¡Correcto!", "Has encontrado al culpable y resuelto el misterio.")
        else:
            messagebox.showinfo("Incorrecto", "La combinación no es correcta. Se generará una nueva combinación.")
            self.configurar_partida()
            self.intentos = 0
            self.mostrar_pantalla_inicio()

    def clear_window(self):
        """Eliminar todos los elementos de la ventana."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Inicializar la aplicación Tkinter
root = tk.Tk()
app = ClueGame(root)
root.mainloop()
