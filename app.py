import tkinter as tk

# Crear la ventana
ventana = tk.Tk()
ventana.title("Mi ventana Tkinter")

# Crear un botón
boton = tk.Button(ventana, text="Haz clic aquí", command=lambda: print("¡Hola desde Tkinter!"))
boton.pack()

# Mantener la ventana abierta
ventana.mainloop()
