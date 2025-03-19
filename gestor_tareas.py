import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from datetime import datetime
import json


class GestorTareasApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gestor de Tareas")

        # Inicialización de tareas
        self.tasks = []
        self.load_tasks()

        # Etiqueta del título
        self.title_label = tk.Label(self.master, text="Gestor de Tareas", font=("Arial", 18))
        self.title_label.pack()

        # Contador de tareas pendientes
        self.pending_label = tk.Label(self.master, text="Tareas Pendientes: 0")
        self.pending_label.pack()

        # Barra de progreso
        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
        self.progress.pack()

        # Lista de tareas
        self.task_listbox = tk.Listbox(self.master, width=50, height=10)
        self.task_listbox.pack()

        # Botón para agregar tarea
        self.add_task_button = tk.Button(self.master, text="Agregar Tarea", command=self.add_task)
        self.add_task_button.pack()

        # Botón para eliminar tarea
        self.delete_task_button = tk.Button(self.master, text="Eliminar Tarea", command=self.delete_task)
        self.delete_task_button.pack()

        # Botón para editar tarea
        self.edit_task_button = tk.Button(self.master, text="Editar Tarea", command=self.edit_task)
        self.edit_task_button.pack()

        # Botón para filtrar por prioridad
        self.filter_priority_button = tk.Button(self.master, text="Filtrar por Prioridad", command=self.filter_by_priority)
        self.filter_priority_button.pack()

        # Botón para filtrar por vencimiento
        self.filter_due_button = tk.Button(self.master, text="Filtrar por Vencimiento", command=self.filter_by_due)
        self.filter_due_button.pack()

        # Botón para ver todas las tareas
        self.show_all_button = tk.Button(self.master, text="Ver Todas las Tareas", command=self.show_all_tasks)
        self.show_all_button.pack()

    def add_task(self):
        task_name = simpledialog.askstring("Nueva Tarea", "Ingresa el nombre de la tarea:")
        if task_name:
            priority = simpledialog.askstring("Prioridad", "Ingresa la prioridad (Alta, Media, Baja):")
            due_date = self.ask_due_date()
            if priority in ["Alta", "Media", "Baja"]:
                task = {"name": task_name, "priority": priority, "due_date": due_date, "completed": False}
                self.tasks.append(task)
                self.update_task_list()
                self.update_progress()
                self.save_tasks()

    def edit_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            task = self.tasks[task_index]

            new_name = simpledialog.askstring("Editar Tarea", "Nuevo nombre de la tarea:", initialvalue=task["name"])
            if new_name:
                task["name"] = new_name

            new_priority = simpledialog.askstring("Editar Prioridad", "Nueva prioridad (Alta, Media, Baja):", initialvalue=task["priority"])
            if new_priority in ["Alta", "Media", "Baja"]:
                task["priority"] = new_priority

            new_due_date = self.ask_due_date(task["due_date"])
            task["due_date"] = new_due_date

            self.update_task_list()
            self.update_progress()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selecciona una tarea", "Primero selecciona una tarea de la lista.")

    def delete_task(self):
        try:
            task_index = self.task_listbox.curselection()[0]
            confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar esta tarea?")
            if confirm:
                del self.tasks[task_index]
                self.update_task_list()
                self.update_progress()
                self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selecciona una tarea", "Primero selecciona una tarea de la lista.")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_info = f"{task['name']} - {task['priority']} - {task['due_date']}"
            self.task_listbox.insert(tk.END, task_info)
        self.update_task_counter()

    def update_task_counter(self):
        pending_tasks = len([task for task in self.tasks if not task["completed"]])
        self.pending_label.config(text=f"Tareas Pendientes: {pending_tasks}")

    def update_progress(self):
        total_tasks = len(self.tasks)
        completed_tasks = len([task for task in self.tasks if task["completed"]])
        progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        self.progress["value"] = progress

    def ask_due_date(self, current_due_date=None):
        date_str = simpledialog.askstring("Fecha de Vencimiento", f"Ingrese la fecha (DD/MM/AAAA):", initialvalue=current_due_date or "")
        try:
            due_date = datetime.strptime(date_str, "%d/%m/%Y")
            return due_date
        except ValueError:
            return None

    def filter_by_priority(self):
        priority = simpledialog.askstring("Filtrar por Prioridad", "Ingrese la prioridad (Alta, Media, Baja):")
        if priority in ["Alta", "Media", "Baja"]:
            filtered_tasks = [task for task in self.tasks if task["priority"] == priority]
            self.update_task_list(filtered_tasks)

    def filter_by_due(self):
        today = datetime.now()
        upcoming_tasks = [task for task in self.tasks if task["due_date"] and task["due_date"] >= today]
        self.update_task_list(upcoming_tasks)

    def show_all_tasks(self):
        self.update_task_list(self.tasks)

    def save_tasks(self):
        with open("tareas.json", "w") as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        try:
            with open("tareas.json", "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []


if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareasApp(root)
    root.mainloop()
