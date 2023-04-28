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

amikos = []
enemikos = []
bidas = 3
dificultad = 1
puntaje = 0
nombre = "ULTRAGAMER"
tiempo = 0

def mas_dificil():
    global dificultad
    while dificultad:
        dificultad += 1
        time.sleep(1)
        
def inicio():
    venjuego = tk.Tk()
    venjuego.configure(bg="#FFFAE4")
    venjuego.title("ACCION")
    venjuego.geometry("1920x1080")

    marcoestat = tk.Frame(venjuego)
    marcoestat.pack(side=tk.TOP, fill=tk.X)
    
    #TODO fondo de estrellitas
    lienzo = tk.Canvas(venjuego, width=1920, height=1000, bg="black")
    lienzo.pack()

    global nombre
    rotnombre = tk.Label(marcoestat, text=str(nombre), font=('Arial', 18))
    rotnombre.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
    
    global bidas
    rotbida = tk.Label(marcoestat, text="vidas: " + str(bidas), font=('Arial', 18))
    rotbida.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    global puntaje
    rotpuntos = tk.Label(marcoestat, text="puntos: " + str(puntaje), font=('Arial', 18))
    rotpuntos.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    global dificultad
    rotnivel = tk.Label(marcoestat, text="nivel: " + str(int(dificultad/60)), font=('Arial', 18))
    rotnivel.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    global tiempo
    rottiempo = tk.Label(marcoestat, text="tiempo: " + str(tiempo), font=('Arial', 18))
    rottiempo.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        
    #bpausa = tk.Button(marcoestat, text="II", command=pausa, font=('Arial', 18))
    #bpausa.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
    
    phjugador = ImageTk.PhotoImage(Image.open("jugador.png"))
    phbala = ImageTk.PhotoImage(Image.open("bala.png"))
    phberde = ImageTk.PhotoImage(Image.open("bichoberde.png")) # pyimage5
    phrojo = ImageTk.PhotoImage(Image.open("bichorojo.png")) # pyimage6

    jugador = lienzo.create_image(150, 540, image=phjugador)

    def estat():
        global enemikos
        colisiones(enemikos, 1)
        for widget in marcoestat.winfo_children():
            widget.destroy()
        global nombre
        rotnombre = tk.Label(marcoestat, text=str(nombre), font=('Arial', 18))
        rotnombre.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
    
        global bidas
        rotbida = tk.Label(marcoestat, text="vidas: " + str(bidas), font=('Arial', 18))
        rotbida.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        global puntaje
        rotpuntos = tk.Label(marcoestat, text="puntos: " + str(puntaje), font=('Arial', 18))
        rotpuntos.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        global dificultad
        rotnivel = tk.Label(marcoestat, text="nivel: " + str(int(dificultad/60)), font=('Arial', 18))
        rotnivel.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        global tiempo
        rottiempo = tk.Label(marcoestat, text="tiempo: " + str(tiempo), font=('Arial', 18))
        rottiempo.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    def reloc():
        while True:
            global tiempo
            global puntaje
            global bidas
            time.sleep(1)
            tiempo += 1
            if tiempo == 58:
                puntaje += 500
            if tiempo == 117:
                puntaje += 2000
            if tiempo == 176:
                puntaje += 10000
            #if bidas <= 0:
                #gameover()
            estat()
    
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
            if objeto != 1:
                lienzo.delete(objeto)
                lienzo.delete(lista[0])
                reciclaje(objeto, 0, 0)
                reciclaje(lista[0], 0, 0)
                estat()
            else:
                global bidas
                bidas -= 1
                lienzo.delete(lista[0])
                reciclaje(lista[0], 0, 0)
                estat()
        else:
            return colisiones(lista[1:], objeto)

             
    def movimiento():

        def arriba(event=None):
            coord = lienzo.bbox(jugador)
            if coord[1] >= 0: 
                lienzo.move(jugador, 0, -25)

        def abajo(event=None):
            coord = lienzo.bbox(jugador)
            if coord[3] <= lienzo.winfo_height():
                lienzo.move(jugador, 0, 25)

        def izquierda(event=None):
            coord = lienzo.bbox(jugador)
            if coord[0] >= 0:
                lienzo.move(jugador, -25, 0)

        def derecha(event=None):
            coord = lienzo.bbox(jugador)
            if coord[2] <= lienzo.winfo_width():
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


    def birus(color):
        bicho = lienzo.create_image(random.randint(1920, 2000), random.randint(50, 950), image=color)

        global enemikos
        enemikos += [bicho]

        if color == phberde:
            xveloz = -2
            if random.randint(0,1):
                yveloz = 2
            else:
                yveloz = -2
        else:
            xveloz = random.randint(-8, -4)
            if random.randint(0,1):
                yveloz = random.randint(4, 8)
            else:
                yveloz = random.randint(-8, -4)
        
        def mov(xveloz, yveloz):
            global amikos
            coord = lienzo.bbox(bicho)
            while (coord != None) and not (colisiones(amikos, bicho)) and coord[2] > 0:
                if (coord[3] >= (lienzo.winfo_height()) or coord[1] < 0):
                    yveloz = -yveloz
                lienzo.move(bicho, xveloz, yveloz)
                time.sleep(0.01)
                coord = lienzo.bbox(bicho)
            global puntaje
            global dificultad
            if coord == None and color == phberde:
                puntaje += dificultad
                estat()
            if coord == None and color == phrojo:
                puntaje += dificultad*4
                estat()
            if (coord != None) and coord[2] < 0:
                lienzo.delete(bicho)
                reciclaje(bicho, 0, 0)

        mov_hilo = Thread(target=mov, args=[xveloz, yveloz])
        mov_hilo.daemon = True
        mov_hilo.start()


    def marsiano():
        bicho = lienzo.create_image(random.randint(1920, 2000), random.randint(50, 950), image=color)

        global enemikos
        enemikos += [bicho]

        if random.randint(0,1):
            yveloz = 6
        else:
            yveloz = -6

        def disparo():
        	coord = lienzo.bbox(bicho)
        	bala = lienzo.create_image(coord[2], coord[3]-50, image=phbalamarsiano)

        	global enemikos
        	enemikos += [bala]
        	
        	def bala_mov():
        	    global amikos
        		coord = lienzo.bbox(bala)
        		while (coord != None) and (coord[2] >= lienzo.winfo_width()) and not (colisiones(amikos, bala)):
        			lienzo.move(bala, -6, 0)
        			time.sleep(0.01)
        			coord = lienzo.bbox(bala)
        		if coord == None or coord[2] < 0:
        		    lienzo.delete(bala)
        		    reciclaje(bala, 0, 0)
        		
        	bala_hilo = Thread(target=bala_mov)
        	bala_hilo.daemon = True
        	bala_hilo.start()

        def mov(yveloz):
            global amikos
            coord = lienzo.bbox(bicho)
            i == 0
            
            while (coord != None) and not (colisiones(amikos, bicho)) and coord[2] > 0:
                global dificultad
                
                if int(dificultad/60) < 1:
                    if i > 1:
                        i = 0
                        disparo_hilo = Thread(target=disparo)
                        disparo_hilo.daemon = True
                        disparo_hilo.start()
                if int(dificultad/60) < 2:
                    if i > 0.5:
                        i = 0
                        disparo_hilo = Thread(target=disparo)
                        disparo_hilo.daemon = True
                        disparo_hilo.start()
                if int(dificultad/60) < 3:
                    if i > 0.25:
                        i = 0
                        disparo_hilo = Thread(target=disparo)
                        disparo_hilo.daemon = True
                        disparo_hilo.start()
                        
                if (coord[3] >= (lienzo.winfo_height()) or coord[1] < 0):
                    yveloz = -yveloz
                lienzo.move(bicho, 0, yveloz)
                time.sleep(0.01)
                coord = lienzo.bbox(bicho)
                i += 0.01
                
            global puntaje
            global dificultad
            puntaje += dificultad*10
            estat()
            
        
    def gen_berde():
        global dificultad
        i = 1
        while dificultad:
            if i > dificultad:
                i = 1
                time.sleep(2)
            else:
                birus(phberde)
                i += 50

    def gen_rojo():
        global dificultad
        i = 1
        while dificultad:
            if dificultad/60 > 1:
                if i > dificultad:
                    i = 1
                    time.sleep(3)
                else:
                    birus(phrojo)
                    i += 100
            else:
                time.sleep(5)

		
    def hilos():
        dif_hilo = Thread(target=mas_dificil)
        dif_hilo.daemon = True
        dif_hilo.start()
        
        mov_hilo = Thread(target=movimiento)
        mov_hilo.daemon = True
        mov_hilo.start()

        tiempo_hilo = Thread(target=reloc)
        tiempo_hilo.daemon = True
        tiempo_hilo.start()
        
        berde_hilo = Thread(target=gen_berde)
        berde_hilo.daemon = True
        berde_hilo.start()

        rojo_hilo = Thread(target=gen_rojo)
        rojo_hilo.daemon = True
        rojo_hilo.start()
        
    hilos()
    venjuego.mainloop()
