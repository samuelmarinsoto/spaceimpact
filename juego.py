import tkinter as tk
import time
import random
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

# TODO: pereguntar a jose sobre try except
amikos = []
enemikos = []
bidas = 3
dificultad = 0.01

def encontrar_i(lista, num, i):
    if lista[i] == num:
        return i
    else:
        return encontrar_i(lista, num, i+1)

def mas_dificil():
    global dificultad
    while dificultad:
        dificultad += 0.01
        time.sleep(0.3)
        
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

    def reciclaje(objeto, i, paso):
        if paso == 0:
            global enemikos
            if i == len(enemikos):
                return reciclaje(objeto, 0, 1)
            elif enemikos[i] == objeto:
                enemikos.pop(i)
                return 0
            else:
                return reciclaje(objeto, i+1, 0)
        else:
            global amikos
            if i == len(amikos):
                return 0
            elif amikos[i] == objeto:
                amikos.pop(i)
                return 0
            else:
                return reciclaje(objeto, i+1, 1)
            

    def colisiones(lista, objeto):
        if lista == []:
            return False
        ocoord = lienzo.bbox(objeto)
        lcoord = lienzo.bbox(lista[0])
        if (lcoord != None) and (ocoord != None) and (lcoord[0] > ocoord[0]) and (lcoord[2] < ocoord[2]) and (lcoord[1] > ocoord[1]) and (lcoord[3] < ocoord[3]):
            lienzo.delete(objeto)
            lienzo.delete(lista[0])
            reciclaje(objeto, 0, 0)
            reciclaje(lista[0], 0, 0)
        else:
            return colisiones(lista[1:], objeto)
                
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

        	global amikos
        	amikos += [bala]
        	
        	def bala_mov():
        		coord = lienzo.bbox(bala)
        		while (coord != None) and (coord[2] <= lienzo.winfo_width()):
        			lienzo.move(bala, 6, 0)
        			time.sleep(0.01)
        			coord = lienzo.bbox(bala)
        		if (coord != None) and coord[2] > lienzo.winfo_width():
        		    lienzo.delete(bala)
        		    reciclaje(bala, 0, 0)
        		
        	bala_hilo = Thread(target=bala_mov)
        	bala_hilo.daemon = True
        	bala_hilo.start()

			
        venjuego.bind('w', arriba)
        venjuego.bind('a', izquierda)
        venjuego.bind('s', abajo)
        venjuego.bind('d', derecha)
        venjuego.bind('<Button-1>', disparo)

    def berde():
    	bicho = lienzo.create_image(random.randint(1400, 1550), random.randint(50, 950), image=phberde)

    	global enemikos
    	enemikos += [bicho]

    	xveloz = random.randint(-4,0)
    	yveloz = random.randint(-4,4)
		
    	def berde_mov(xveloz, yveloz):
    	    global amikos
    	    coord = lienzo.bbox(bicho)
    	    while (coord != None) and not (colisiones(amikos, bicho)) and coord[2] > 0:
    		    if (coord[3] >= (lienzo.winfo_height()) or coord[1] < 0):
    		        yveloz = -yveloz
    		    lienzo.move(bicho, xveloz, yveloz)
    		    time.sleep(0.01)
    		    coord = lienzo.bbox(bicho)
    	    if (coord != None) and coord[2] < 0:
    	        lienzo.delete(bicho)
    	        reciclaje(bicho, 0, 0)

    	mov_hilo = Thread(target=berde_mov, args=[xveloz, yveloz])
    	mov_hilo.daemon = True
    	mov_hilo.start()

    def gen_berde():
        global dificultad
        while dificultad:
            print(dificultad)
            berde()
            time.sleep(dificultad)

			
    def hilos():
        dif_hilo = Thread(target=mas_dificil)
        dif_hilo.daemon = True
        dif_hilo.start()
        
        mov_hilo = Thread(target=movimiento)
        mov_hilo.daemon = True
        mov_hilo.start()

        berde_hilo = Thread(target=gen_berde)
        berde_hilo.daemon = True
        berde_hilo.start()
        
    hilos()
    venjuego.mainloop()
