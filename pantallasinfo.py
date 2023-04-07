import tkinter as tk
from PIL import Image, ImageTk
import pygame

def pantallainicial():
	# abre ventana, con fondo bonito
	menu = tk.Tk()
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

	bsalir = tk.Button(mmenu, text="Salir", font=('Arial', 18), command=salir)
	bsalir.pack(pady=10)
	
	menu.mainloop()

def jugar():
	return 1+1
	
def opciones():
	return 1+1
	
def puntajes():
	return 1+1
	
def salir():
	return 1+1

pantallainicial()
