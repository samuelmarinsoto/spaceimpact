import tkinter as tk
from PIL import Image, ImageTk
import pygame

	
def pantallainicial():
	# abre ventana, con fondo bonito
	menu = tk.Tk()
	for widget in menu.winfo_children():
		widget.pack_forget()
		
	menu.configure(bg="Black")
	menu.title("SPACE IMPACT REMIX")
	menu.geometry("800x600")

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

	# los botones van separados, con colores, y ejecutan las funciones para las otras ventanas
	bjugar = tk.Button(mmenu, text="Jugar", font=('Arial', 18), command=jugar)
	bjugar.pack(pady=10)
	
	bopciones = tk.Button(mmenu, text="Opciones", font=('Arial', 18), command=opciones)
	bopciones.pack(pady=10)
	
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
		menu.destroy()
		
	bsalir = tk.Button(mmenu, text="Salir", font=('Arial', 18), command=salir)
	bsalir.pack(pady=10)
	
	menu.mainloop()
		
def jugar():
	return 1+1
	
def opciones():
	return 1+1
	
def puntajes():
	return 1+1

pantallainicial()
