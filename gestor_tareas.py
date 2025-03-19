import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Gestor de Tareas")
ventana.geometry("500x500")

# Lista para almacenar las tareas
tareas = []

# Función para agregar tarea con fecha
def agregar_tarea():
    tarea = cuadro_entrada.get()  # Obtener texto de entrada
    fecha = simpledialog.askstring("Fecha de Tarea", "Introduce la fecha (DD/MM/YYYY):")  # Pedir fecha

    # Validar que la tarea no esté vacía y la fecha tenga el formato correcto
    try:
        fecha_formateada = datetime.strptime(fecha, "%d/%m/%Y").strftime("%d/%m/%Y")
        if tarea != "":
            tareas.append((tarea, fecha_formateada))  # Guardar la tarea con la fecha
            actualizar_lista()  # Actualizar la lista mostrada
            cuadro_entrada.delete(0, tk.END)  # Limpiar el cuadro de entrada
    except ValueError:
        # Si la fecha no es válida, mostrar un error
        tk.messagebox.showerror("Error", "Por favor, introduce una fecha válida en formato DD/MM/YYYY.")

# Función para eliminar tarea seleccionada
def eliminar_tarea():
    tarea_seleccionada = lista_tareas.curselection()  # Obtener tarea seleccionada
    if tarea_seleccionada:
        tarea = lista_tareas.get(tarea_seleccionada)  # Obtener el texto de la tarea
        tareas.remove((tarea.split(" | ")[0], tarea.split(" | ")[1]))  # Eliminar la tarea de la lista
        actualizar_lista()  # Actualizar la lista mostrada

# Función para marcar tarea como completada
def completar_tarea():
    tarea_seleccionada = lista_tareas.curselection()  # Obtener tarea seleccionada
    if tarea_seleccionada:
        tarea = lista_tareas.get(tarea_seleccionada)  # Obtener la tarea seleccionada
        tarea_completada = tarea + " (Completada)"  # Texto de tarea completada
        tareas[tareas.index((tarea.split(" | ")[0], tarea.split(" | ")[1]))] = (tarea.split(" | ")[0] + " (Completada)", tarea.split(" | ")[1])  # Reemplazar en la lista
        actualizar_lista()  # Actualizar la lista mostrada

# Función para actualizar el Listbox con las tareas
def actualizar_lista():
    lista_tareas.delete(0, tk.END)  # Limpiar lista actual
    for tarea, fecha in tareas:  # Agregar tareas con fecha a la lista
        lista_tareas.insert(tk.END, f"{tarea} | {fecha}")

# Crear cuadro de entrada para nueva tarea
cuadro_entrada = tk.Entry(ventana, width=40)
cuadro_entrada.pack(pady=10)

# Crear botón para agregar tarea
boton_agregar = tk.Button(ventana, text="Agregar Tarea", width=20, command=agregar_tarea)
boton_agregar.pack(pady=5)

# Crear lista de tareas
lista_tareas = tk.Listbox(ventana, width=40, height=10)
lista_tareas.pack(pady=10)

# Crear botón para eliminar tarea
boton_eliminar = tk.Button(ventana, text="Eliminar Tarea", width=20, command=eliminar_tarea)
boton_eliminar.pack(pady=5)

# Crear botón para marcar tarea como completada
boton_completar = tk.Button(ventana, text="Marcar como completada", width=20, command=completar_tarea)
boton_completar.pack(pady=5)

# Iniciar el bucle principal de la ventana
ventana.mainloop()
