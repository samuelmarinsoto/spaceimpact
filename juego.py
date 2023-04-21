import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
import pygame

def inicio():
    venjuego = tk.Tk()
    venjuego.configure(bg="#FFFAE4")
    venjuego.title("ACCION")
    venjuego.geometry("1000x1600")

    #TODO fondo de estrellitas
    lienzo = tk.Canvas(venjuego, width=1000, height=900, bg="black")
    lienzo.pack()

    imjugador = Image.open("jugador.png")
    phjugador = ImageTk.PhotoImage(imjugador)
    jugador = lienzo.create_image(0, 500, image=phjugador)

    def movimiento():
        def arriba(event=None):
            lienzo.move(jugador, 0, -50)
        def abajo(event=None):
            lienzo.move(jugador, 0, 50)
        def izquierda(event=None):
            lienzo.move(jugador, -50, 0)
        def derecha(event=None):
            lienzo.move(jugador, 50, 0)

        venjuego.bind('w', arriba)
        venjuego.bind('a', izquierda)
        venjuego.bind('s', abajo)
        venjuego.bind('d', derecha)

    def hilos():
        movimiento_hilo = Thread(target=movimiento)
        movimiento_hilo.daemon = True
        movimiento_hilo.start()

    hilos()
    venjuego.mainloop()
