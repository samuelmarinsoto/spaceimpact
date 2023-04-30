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
bidaselec = 3
dificultad = 1
difselec = 1
puntaje = 0
nombre = "ULTRAGAMER"
tiempo = 0

def pantallainicial():
	pygame.mixer.init(48000)
	pygame.mixer.music.load("menu.ogg")
	pygame.mixer.music.play()
	
	# abre ventana, con fondo bonito
	menu = tk.Tk()
	for widget in menu.winfo_children():
		widget.pack_forget()
			
	menu.configure(bg="Black")
	menu.title("SPACE IMPACT REMIX")
	menu.geometry("800x800")
	
	mnombre = tk.Frame(menu)
	mnombre.pack(side=tk.TOP)
	mnombre.configure(bg="Black")
	
	im = Image.open("spaceimpactlogomini.png")
	ph = ImageTk.PhotoImage(im)

	logo = tk.Label(mnombre, image=ph)
	logo.pack(side=tk.TOP, pady=30)
	logo.configure(bg="Black")
	
	mmenu = tk.Frame(menu)
	mmenu.pack()
	mmenu.configure(bg="Black")
	
	def jugar():
		menu.destroy()
		inicio()
	
	# los botones van separados, con colores, y ejecutan las funciones para las otras ventanas
	bjugar = tk.Button(mmenu, text="Jugar", font=('Arial', 18), command=jugar)
	bjugar.pack(pady=10)
	
	def opciones():
		for widget in menu.winfo_children():
			widget.pack_forget()
	
		mtexto = tk.Frame(menu, width=500, height=500, bg="black")
		mtexto.pack(padx=150, pady=150)

		marriba = tk.Frame(mtexto)
		marriba.pack(side=tk.TOP, pady=10)
		marriba.configure(bg="Black")

		mrotdif = tk.Frame(mtexto, bg="black")
		mrotdif.pack()
	
		rotnombre = tk.Label(marriba, text="Nombre: ", font=('Arial', 18), bg="black", fg="white")
		rotnombre.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
	
		entrada = tk.Entry(marriba)
		entrada.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
	
		def confnombre():
			global nombre
			nombre = entrada.get()
	
		btnok = tk.Button(marriba, text="OK", font=('Arial', 18), command=confnombre)
		btnok.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

		rotdificultad = tk.Label(mrotdif, text="Dificultad: Normal", font=('Arial', 18), bg="black", fg="white")
		rotdificultad.pack(expand=True, fill=tk.BOTH)
	
		def confdificultad(d, b):
			global difselec
			global bidaselec
			difselec = d
			bidaselec = b

		def repackrotdif(dif):
			for widget in mrotdif.winfo_children():
				widget.destroy()
			rotdificultad = tk.Label(mrotdif, text="Dificultad: " + dif, font=('Arial', 18), bg="black", fg="white")
			rotdificultad.pack(expand=True, fill=tk.BOTH)
			
		def facil():
			confdificultad(1,6)
			repackrotdif("Facil")

		def normal():
			confdificultad(60, 3)
			repackrotdif("Normal")

		def pesadilla():
			confdificultad(240, 1)
			repackrotdif("PESADILLA")

		btn1 = tk.Button(mtexto, text="Facil", font=('Arial', 18), command=facil)
		btn1.pack()
		btn2 = tk.Button(mtexto, text="Normal", font=('Arial', 18), command=normal)
		btn2.pack()
		btn3 = tk.Button(mtexto, text="PESADILLA", font=('Arial', 18), command=pesadilla)
		btn3.pack()
	
		def repackinicial():
			mtexto.destroy()
			mregresar.destroy()
			
			mnombre.pack(side=tk.TOP)
			logo.pack(side=tk.TOP, pady=30)
			mmenu.pack()
			bjugar.pack(pady=10)
			bopciones.pack(pady=10)
			bpuntajes.pack(pady=10)
			bcreditos.pack(pady=10)
			bsalir.pack(pady=10)
				
		mregresar = tk.Frame(menu)
		mregresar.pack(anchor="sw")
		mregresar.configure(bg="Black")
			
		bregresar = tk.Button(mregresar, text="Regresar", font=('Arial', 14), command=repackinicial)
		bregresar.pack()
			
	bopciones = tk.Button(mmenu, text="Opciones", font=('Arial', 18), command=opciones)
	bopciones.pack(pady=10)

	def puntajes():
		for widget in menu.winfo_children():
			widget.pack_forget()

		rottexto = tk.Label(menu, text="Puntajes", bg="black", fg="white", font=('Arial', 24))
		rottexto.pack(pady=20, side=tk.TOP)

		with open("puntajes.txt") as f:
		    lineas = f.read().splitlines()
		
		def partir(lineas, puntajes):
			if lineas == []:
				return puntajes
			else:
				l = lineas[0].split()
				l = [l[0]] + [int(l[1])]
				return partir(lineas[1:], puntajes + [l])

		def sortear(lista, n, i):
			if i == 0:
				return lista
			elif n == 0:
				i -= 1
				return sortear(lista, len(lista)-1, i)
			else:		
				if lista[n-1][1] < lista[n][1]:
					temp = lista[n][1]
					lista[n][1] = lista[n-1][1]
					lista[n-1][1] = temp
					return sortear(lista, n-1, i)
				else:
					return sortear(lista, n-1, i)

		puntajes = partir(lineas, [])
		puntajes = sortear(puntajes, len(puntajes)-1, len(puntajes)-1)
		puntajes = puntajes[:7]

		rotpuntajes = tk.Label(menu, text="#1 " + puntajes[0][0] + " " + str(puntajes[0][1]) + "\n" + \
		"#2 " + puntajes[1][0] + " " + str(puntajes[1][1]) + "\n" + \
		"#3 " + puntajes[2][0] + " " + str(puntajes[2][1]) + "\n" + \
		"#4 " + puntajes[3][0] + " " + str(puntajes[3][1]) + "\n" + \
		"#5 " + puntajes[4][0] + " " + str(puntajes[4][1]) + "\n" + \
		"#6 " + puntajes[5][0] + " " + str(puntajes[5][1]) + "\n" + \
		"#7 " + puntajes[6][0] + " " + str(puntajes[6][1]) + "\n", bg="black", fg="white", font=('Arial', 18), justify=tk.LEFT)
		rotpuntajes.pack()

		mregresar = tk.Frame(menu)
		mregresar.pack(anchor="sw")
		mregresar.configure(bg="Black")
	
		def repackinicial():
			rottexto.destroy()
			rotpuntajes.destroy()
			mregresar.destroy()
			
			mnombre.pack(side=tk.TOP)
			logo.pack(side=tk.TOP, pady=30)
			mmenu.pack()
			bjugar.pack(pady=10)
			bopciones.pack(pady=10)
			bpuntajes.pack(pady=10)
			bcreditos.pack(pady=10)
			bsalir.pack(pady=10)
		
		bregresar = tk.Button(mregresar, text="Regresar", font=('Arial', 14), command=repackinicial)
		bregresar.pack()
			
	
	bpuntajes = tk.Button(mmenu, text="Puntajes", font=('Arial', 18), command=puntajes)
	bpuntajes.pack(pady=10)
	
	imcred = Image.open("yo.png")
	phcred = ImageTk.PhotoImage(imcred)
			
	def creditos():
		for widget in menu.winfo_children():
			widget.pack_forget()
	
		marriba = tk.Frame(menu)
		marriba.pack(side=tk.TOP, pady=10)
		marriba.configure(bg="Black")
			
		mfoto = tk.Frame(marriba)
		mfoto.pack(side=tk.LEFT, padx=10)
		mfoto.configure(bg="Black")
	
		foto = tk.Label(mfoto, image=phcred)
		foto.pack()
		foto.configure(bg="Black")
			
		mcred = tk.Frame(marriba)
		mcred.pack()
		mcred.configure(bg="Black")
		
		rtitulo = tk.Label(mcred, text="Creditos", font=('Arial', 20), justify=tk.CENTER, bg="Black", fg="White")
		rtitulo.pack(side=tk.TOP)
		
		rinfo = tk.Label(mcred, text="Autor: Samuel Marin Soto\nCarne: 2023073212\nInstitucion: ITCR\nAsignatura: Primer Projecto de Taller, Juego Space Impact\nCarrera: Ingenieria en Computadores\nAno: 2023\nProfesor: Jeff Schmidt Peralta\nProducido en Costa Rica\nVersion: 0.1", font=('Arial', 12), justify=tk.CENTER, bg="Black", fg="White")
		rinfo.pack()
		
		mregresar = tk.Frame(menu)
		mregresar.pack(anchor="sw")
		mregresar.configure(bg="Black")
	
		def repackinicial():
			marriba.destroy()
			mregresar.destroy()
			
			mnombre.pack(side=tk.TOP)
			logo.pack(side=tk.TOP, pady=30)
			mmenu.pack()
			bjugar.pack(pady=10)
			bopciones.pack(pady=10)
			bpuntajes.pack(pady=10)
			bcreditos.pack(pady=10)
			bsalir.pack(pady=10)
		
		bregresar = tk.Button(mregresar, text="Regresar", font=('Arial', 14), command=repackinicial)
		bregresar.pack()
	
	bcreditos = tk.Button(mmenu, text="Creditos", font=('Arial', 18), command=creditos)
	bcreditos.pack(pady=10)
	
	def salir():
		pygame.mixer.music.stop()
		pygame.mixer.music.unload()
		menu.destroy()
			
	bsalir = tk.Button(mmenu, text="Salir", font=('Arial', 18), command=salir)
	bsalir.pack(pady=10)
		
	menu.mainloop()
	
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

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("juego.ogg")
    pygame.mixer.music.play()

    marcoestad = tk.Frame(venjuego)
    marcoestad.pack(side=tk.TOP, fill=tk.X)
    
    #TODO fondo de estrellitas
    lienzo = tk.Canvas(venjuego, width=1920, height=1040, bg="black")
    lienzo.pack()

    global nombre
    rotnombre = tk.Label(marcoestad, text=str(nombre), font=('Arial', 18))
    rotnombre.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
    
    global bidas
    global bidaselec
    bidas = bidaselec
    rotbida = tk.Label(marcoestad, text="Vidas: " + str(bidas), font=('Arial', 18))
    rotbida.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    global puntaje
    puntaje = 0
    rotpuntos = tk.Label(marcoestad, text="Puntos: " + str(puntaje), font=('Arial', 18))
    rotpuntos.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    global dificultad
    global difselec
    dificultad = difselec
    rotnivel = tk.Label(marcoestad, text="Nivel: " + str(int(dificultad/60)), font=('Arial', 18))
    rotnivel.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    global enemikos
    rotenemikos = tk.Label(marcoestad, text="Enemigos: " + str(len(enemikos)), font=('Arial', 18))
    rotenemikos.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    global tiempo
    tiempo = 0
    rottiempo = tk.Label(marcoestad, text="tiempo: " + str(tiempo), font=('Arial', 18))
    rottiempo.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

    def rendirse():
    	for widget in venjuego.winfo_children():
    		widget.destroy()
    	seacabo()

    btnrendirse = tk.Button(marcoestad, text="RENDIRSE", font=('Arial', 18), command=rendirse)
    btnrendirse.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
    
    phjugador = ImageTk.PhotoImage(Image.open("jugador.png"))
    phbala = ImageTk.PhotoImage(Image.open("bala.png"))
    phberde = ImageTk.PhotoImage(Image.open("bichoberde.png")) # pyimage5
    phrojo = ImageTk.PhotoImage(Image.open("bichorojo.png")) # pyimage6
    phmarsiano = ImageTk.PhotoImage(Image.open("marsiano.png")) # pyimage7
    phmisil = ImageTk.PhotoImage(Image.open("misil.png")) # pyimage8

    jugador = lienzo.create_image(150, 540, image=phjugador)
		
    def seacabo():
    	pygame.mixer.music.stop()
    	pygame.mixer.music.unload()
    	pygame.mixer.music.load("sad.ogg")
    	pygame.mixer.music.play()
    	
    	venjuego.title("PERDISTE")
    	venjuego.geometry("800x800")
    	
    	marcotexto = tk.Frame(venjuego, width=500, height=500, bg="#FFFAE4")
    	marcotexto.pack(padx=150, pady=150)

    	global nombre
    	global puntaje
    	rottexto = tk.Label(marcotexto, text="PERDISTE EL JUEGO", font=('Arial', 24))
    	rottexto.configure(bg="#FFFAE4")
    	rottexto.pack(side=tk.TOP)
    	rotestad = tk.Label(marcotexto, text="JUGADOR: " + str(nombre) + "\nPUNTAJE: " + str(puntaje), font=('Arial', 18))
    	rotestad.configure(bg="#FFFAE4")
    	rotestad.pack(pady=10)

    	def salir():
    		with open("puntajes.txt", "a") as archivo:
    		    archivo.write(nombre + ": " + str(puntaje) + "\n")
    		venjuego.destroy()

    	def regresar():
    		with open("puntajes.txt", "a") as archivo:
    			archivo.write(nombre + ": " + str(puntaje) + "\n")
    		venjuego.destroy()
    		pantallainicial()

    	def reintentar():
    		with open("puntajes.txt", "a") as archivo:
    			archivo.write(nombre + ": " + str(puntaje) + "\n")
    		venjuego.destroy()
    		inicio()

    	btnreintentar = tk.Button(marcotexto, text="Reintentar", font=('Arial', 18), command=reintentar)
    	btnreintentar.pack()
    	btnregresar = tk.Button(marcotexto, text="Regresar a menu", font=('Arial', 18), command=regresar)
    	btnregresar.pack()
    	btnsalir = tk.Button(marcotexto, text="Salir", font=('Arial', 18), command=salir)
    	btnsalir.pack()
		
		
    def estad():
        global enemikos
        colisiones(enemikos, 1)
        for widget in marcoestad.winfo_children():
            widget.destroy()
        global nombre
        rotnombre = tk.Label(marcoestad, text=str(nombre), font=('Arial', 18))
        rotnombre.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
    
        global bidas
        rotbida = tk.Label(marcoestad, text="Vidas: " + str(bidas), font=('Arial', 18))
        rotbida.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        global puntaje
        rotpuntos = tk.Label(marcoestad, text="Puntos: " + str(puntaje), font=('Arial', 18))
        rotpuntos.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        global dificultad
        rotnivel = tk.Label(marcoestad, text="Nivel: " + str(int(dificultad/60)), font=('Arial', 18))
        rotnivel.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        rotenemikos = tk.Label(marcoestad, text="Enemigos: " + str(len(enemikos)), font=('Arial', 18))
        rotenemikos.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        global tiempo
        rottiempo = tk.Label(marcoestad, text="Tiempo: " + str(tiempo), font=('Arial', 18))
        rottiempo.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        btnrendirse = tk.Button(marcoestad, text="RENDIRSE", font=('Arial', 18), command=rendirse)
        btnrendirse.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

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
            if bidas <= 0:
            	for widget in venjuego.winfo_children():
            		widget.destroy()
            	seacabo()
            estad()
    
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
        o = lienzo.bbox(objeto)
        l = lienzo.bbox(lista[0])
        if (l != None) and (o != None) and (\
        (o[0] < l[0] < o[2] < l[2] and l[1] < o[1] < l[3] < o[3]) or \
        (o[0] < l[0] < o[2] < l[2] and o[1] < l[1] < o[3] < l[3]) or \
        (l[0] < o[0] < l[2] < o[2] and o[1] < l[1] < o[3] < l[3]) or \
        (l[0] < o[0] < l[2] < o[2] and l[1] < o[1] < l[3] < o[3]) or \
        (l[0] < o[0] < o[2] < l[2] and l[1] < o[1] < o[3] < l[3]) or \
        (o[0] < l[0] < l[2] < o[2] and o[1] < l[1] < l[3] < o[3])):
            if objeto != 1:
                lienzo.delete(objeto)
                lienzo.delete(lista[0])
                reciclaje(objeto, 0, 0)
                reciclaje(lista[0], 0, 0)
                estad()
            else:
                global bidas
                bidas -= 1
                lienzo.delete(lista[0])
                reciclaje(lista[0], 0, 0)
                estad()
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
                estad()
            if coord == None and color == phrojo:
                puntaje += dificultad*4
                estad()
            if (coord != None) and coord[2] < 0:
                lienzo.delete(bicho)
                reciclaje(bicho, 0, 0)

        mov_hilo = Thread(target=mov, args=[xveloz, yveloz])
        mov_hilo.daemon = True
        mov_hilo.start()


    def marsiano():
        bicho = lienzo.create_image(random.randint(1800, 1900), random.randint(100, 900), image=phmarsiano)

        global enemikos
        enemikos += [bicho]

        if random.randint(0,1):
            yveloz = 6
        else:
            yveloz = -6

        def mov(yveloz):
            global amikos
            coord = lienzo.bbox(bicho)
            i = 0
            
            def disparo():
            	bala = lienzo.create_image(coord[0], coord[3]-37, image=phmisil)

            	global enemikos
            	enemikos += [bala]

            	def bala_mov():
            		global amikos
            		coord = lienzo.bbox(bala)

            		while (coord != None) and (coord[2] >= 0) and not (colisiones(amikos, bala)):
            			lienzo.move(bala, -12, 0)
            			time.sleep(0.01)
            			coord = lienzo.bbox(bala)
            		if coord == None or coord[2] < 0:
            			lienzo.delete(bala)
            			reciclaje(bala, 0, 0)

            	bala_hilo = Thread(target=bala_mov)
            	bala_hilo.daemon = True
            	bala_hilo.start()

            while (coord != None) and not (colisiones(amikos, bicho)) and coord[2] > 0:
                global dificultad
                
                if dificultad > 120 and dificultad < 150:
                    if i > 1:
                        i = 0
                        disparo_hilo = Thread(target=disparo)
                        disparo_hilo.daemon = True
                        disparo_hilo.start()
                if dificultad > 150 and dificultad < 180:
                    if i > 0.5:
                        i = 0
                        disparo_hilo = Thread(target=disparo)
                        disparo_hilo.daemon = True
                        disparo_hilo.start()
                if dificultad > 180:
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
            puntaje += dificultad*10
            estad()

        mov_hilo = Thread(target=mov, args=[yveloz])
        mov_hilo.daemon = True
        mov_hilo.start()
            
        
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
                time.sleep(3)

    def gen_marsiano():
    	global dificultad
    	i = 1
    	while dificultad:
    		if dificultad/60 > 2:
    			if i > dificultad:
    				i = 1
    				time.sleep(5)
    			else:
    				marsiano()
    				i += 200
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

        marsiano_hilo = Thread(target=gen_marsiano)
        marsiano_hilo.daemon = True
        marsiano_hilo.start()
        
    hilos()
    venjuego.mainloop()

pantallainicial()
