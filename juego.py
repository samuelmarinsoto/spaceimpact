import tkinter as tk
import time
from PIL import Image, ImageTk
from threading import Thread
import pygame

# TODO: lista global de todas las balas amikas y otra lista global con todas las balas enemikas. 
#
# Al meter una imagen en el lienzo, la funcion lienzo.create_image retorna un entero para identificar 
# a la imagen, y este se puede usar con otras funciones del lienzo para ver coordenadas y borrar la imagen. 
#
# nuevas balas se anaden a las listas con concatenacion.
#
# los enemikos checkean (a travez de una funcion externa talvez) si alguna bala de la lista de balas amikas los toco
# (itera sobre toda la lista, checkeando las coords de cada elemento con lienzo.bbox). si los toco, en la funcion del 
# enemigo se borra al enemigo, y se borra la bala del lienzo (usando el entero de la bala). 
#
# se puede quitar la bala de lista global con slicing[1][2]. 
#
# luego mismo vara para quitar vidas pero con lo de balas enemikas. en el codigo de las balas, 
# las amikas puede checkear si una bala enemika los toco y asi se desaparecen y desaparecen a la bala que las toco, y se
# sacan las dos de sus listas respectivas con slicing[1][2]
#
# [1] al borrar las balas, la funcion lienzo.bbox(bala) va a retornan None evenz de las coordenadas, entonces checkearlas es crinch,
# mejor evitar
#
# [2] otro problema es una condicion de carrera entre las balas amikas y enemikas. si una itera y encuentra que toco
# a la otra, se va a desaparecer y mandar pa fuera antes de que la otra haga lo mismo, entonces la otra nunca desaparece

def inicio():
    venjuego = tk.Tk()
    venjuego.configure(bg="#FFFAE4")
    venjuego.title("ACCION")
    venjuego.geometry("1600x1000")

    #TODO fondo de estrellitas
    lienzo = tk.Canvas(venjuego, width=1600, height=1000, bg="black")
    lienzo.pack()

    phjugador = ImageTk.PhotoImage(Image.open("jugador.png"))
    phbala = ImageTk.PhotoImage(Image.open("bala.png"))
    phberde = ImageTk.PhotoImage(Image.open("bichoberde.png"))

    jugador = lienzo.create_image(0, 500, image=phjugador)
	
    def movimiento():

        def arriba(event=None):
            lienzo.move(jugador, 0, -25)

        def abajo(event=None):
            lienzo.move(jugador, 0, 25)

        def izquierda(event=None):
            lienzo.move(jugador, -25, 0)

        def derecha(event=None):
        	lienzo.move(jugador, 25, 0)

        def disparo(event=None):
        	jugador_coord = lienzo.bbox(jugador)
        	bala = lienzo.create_image(jugador_coord[2], jugador_coord[3]-50, image=phbala)
        	
        	def bala_mov():
        		bala_coord = lienzo.bbox(bala)
        		while bala_coord[2] < lienzo.winfo_width():
        			bala_coord = lienzo.bbox(bala)
        			print(bala_coord)
        			time.sleep(0.01)
        			lienzo.move(bala, 6, 0)
        		print(bala)
        		lienzo.delete(bala)
	
        	bala_hilo = Thread(target=bala_mov)
        	bala_hilo.daemon = True
        	bala_hilo.start()
			
        venjuego.bind('w', arriba)
        venjuego.bind('a', izquierda)
        venjuego.bind('s', abajo)
        venjuego.bind('d', derecha)
        venjuego.bind('k', disparo)

    def berde():
    	bicho = lienzo.create_image(random.randint(1400, 1550), random.randint(50, 950), image=phberde)

    	def berde_mov():
    		berde_coord = lienzo.bbox(bicho)

    def bichos():
    	berde()
			
    def hilos():
        movimiento_hilo = Thread(target=movimiento)
        movimiento_hilo.daemon = True
        movimiento_hilo.start()

    hilos()
    venjuego.mainloop()
