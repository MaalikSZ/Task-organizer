import tkinter as tk
from tkinter import messagebox, filedialog

tasks = []

def add_task():
    title = title_entry.get()
    description = description_entry.get()
    tasks.append({"tytuł": title, "opis": description, "ukończone": False})
    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    display_tasks()

def display_tasks():
    tasks_text.delete(1.0, tk.END)
    if not tasks:
        tasks_text.insert(tk.END, "Brak zadań.")
    else:
        for index, task in enumerate(tasks, start=1):
            status = "ukończone" if task["ukończone"] else "nieukończone"
            tasks_text.insert(tk.END, f"{index}. {task['tytuł']} - {task['opis']} [{status}]\n")

def mark_as_completed():
    index = int(index_entry.get()) - 1
    if 0 <= index < len(tasks):
        tasks[index]["ukończone"] = True
        index_entry.delete(0, tk.END)
        display_tasks()
    else:
        index_entry.delete(0, tk.END)
        messagebox.showerror("Error", "Nieprawidłowy indeks zadania.")

def delete_task():
    index = int(index_entry.get()) - 1
    if 0 <= index < len(tasks):
        del tasks[index]
        index_entry.delete(0, tk.END)
        display_tasks()
    else:
        index_entry.delete(0, tk.END)
        messagebox.showerror("Error", "Nieprawidłowy indeks zadania.")

def save_to_file():
    if tasks:
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    for task in tasks:
                        status = "Ukończone" if task["ukończone"] else "nieukończone"
                        file.write(f"Tytuł: {task['tytuł']}\n")
                        file.write(f"Opis: {task['opis']}\n")
                        file.write(f"Status: {status}\n")
                        file.write("-" * 20 + "\n")
                tasks_text.delete(1.0, tk.END)
                tasks_text.insert(tk.END, f"Zadania zostały zapisane w: {file_path}.")
        except IOError:
            tasks_text.delete(1.0, tk.END)
            messagebox.showerror("Error", "Błąd podczas zapisywania pliku.")
    else:
        tasks_text.delete(1.0, tk.END)
        messagebox.showinfo("Uwaga", "Brak zadań do zapisania.")

def load_from_file():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Pliki tekstowe", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                tasks.clear()
                title = None
                description = None
                completed = False
                for line in file:
                    if line.strip().startswith("Tytuł:"):
                        title = line.strip().split(":")[1].strip()
                    elif line.strip().startswith("Opis:"):
                        description = line.strip().split(":")[1].strip()
                    elif line.strip().startswith("Status:"):
                        status = line.strip().split(":")[1].strip()
                        completed = True if status == "Ukończone" else False
                    elif line.strip() == "-" * 20:
                        tasks.append({"tytuł": title, "opis": description, "ukończone": completed})
                        title = None
                        description = None
                        completed = False
                display_tasks()
                tasks_text.delete(1.0, tk.END)
                tasks_text.insert(tk.END, f"Zadania zostały wczytane z: {file_path}.")
    except FileNotFoundError:
        tasks_text.delete(1.0, tk.END)
        messagebox.showerror("Error", "Plik nie istnieje.")
    except IOError:
        tasks_text.delete(1.0, tk.END)
        messagebox.showerror("Error", "Błąd podczas wczytywania pliku.")

def delete_all_tasks():
    if tasks:
        result = messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz usunąć wszystkie zadania?")
        if result == "yes":
            tasks.clear()
            display_tasks()
    else:
        messagebox.showinfo("Uwaga", "Brak zadań do usunięcia.")

def search_tasks():
    keyword = search_entry.get().lower()
    matching_tasks = [task for task in tasks if keyword in task['tytuł'].lower() or keyword in task['opis'].lower()]
    tasks_text.delete(1.0, tk.END)
    if not matching_tasks:
        tasks_text.insert(tk.END, "Brak pasujących zadań.")
    else:
        for index, task in enumerate(matching_tasks, start=1):
            status = "ukończone" if task["ukończone"] else "nieukończone"
            tasks_text.insert(tk.END, f"{index}. {task['tytuł']} - {task['opis']} [{status}]\n")

def clear_entries():
    title_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    index_entry.delete(0, tk.END)
    search_entry.delete(0, tk.END)

def exit_application():
    result = messagebox.askquestion("Potwierdzenie", "Czy na pewno chcesz zamknąć aplikację?")
    if result == "yes":
        root.destroy()

root = tk.Tk()
root.title("Organizer zadań")

input_frame = tk.LabelFrame(root, text="Dodaj zadanie", padx=10, pady=10)
input_frame.pack(padx=10, pady=10, fill="both", expand=True)

title_label = tk.Label(input_frame, text="Tytuł zadania:")
title_label.grid(row=0, column=0, sticky="W")

title_entry = tk.Entry(input_frame, width=30)
title_entry.grid(row=0, column=1, padx=5, pady=5)

description_label = tk.Label(input_frame, text="Opis zadania:")
description_label.grid(row=1, column=0, sticky="W")

description_entry = tk.Entry(input_frame, width=30)
description_entry.grid(row=1, column=1, padx=5, pady=5)

buttons_frame = tk.Frame(root)
buttons_frame.pack(padx=10, pady=(0, 10))

add_button = tk.Button(buttons_frame, text="Dodaj zadanie", command=add_task)
add_button.grid(row=0, column=0, padx=5)

display_button = tk.Button(buttons_frame, text="Pokaż zadania", command=display_tasks)
display_button.grid(row=0, column=1, padx=5)

search_label = tk.Label(buttons_frame, text="Szukaj:")
search_label.grid(row=1, column=0, padx=5, pady=(10, 0))

search_entry = tk.Entry(buttons_frame, width=30)
search_entry.grid(row=1, column=1, padx=5, pady=(10, 0))

search_button = tk.Button(buttons_frame, text="Szukaj zadania", command=search_tasks)
search_button.grid(row=2, column=0, columnspan=2, pady=(5, 0))

index_label = tk.Label(buttons_frame, text="Indeks zadania:")
index_label.grid(row=3, column=0, padx=5, pady=(10, 0))

index_entry = tk.Entry(buttons_frame, width=30)
index_entry.grid(row=3, column=1, padx=5, pady=(10, 0))

mark_button = tk.Button(buttons_frame, text="Zaznacz jako ukończone", command=mark_as_completed)
mark_button.grid(row=4, column=0, columnspan=2, pady=(5, 0))

delete_button = tk.Button(buttons_frame, text="Usuń zadanie", command=delete_task)
delete_button.grid(row=5, column=0, columnspan=2, pady=(5, 0))

save_button = tk.Button(buttons_frame, text="Zapisz do pliku", command=save_to_file)
save_button.grid(row=6, column=0, columnspan=2, pady=(5, 0))

load_button = tk.Button(buttons_frame, text="Wczytaj z pliku", command=load_from_file)
load_button.grid(row=7, column=0, columnspan=2, pady=(5, 0))

delete_all_button = tk.Button(buttons_frame, text="Usuń wszystkie zadania", command=delete_all_tasks)
delete_all_button.grid(row=8, column=0, columnspan=2, pady=(5, 0))

clear_button = tk.Button(buttons_frame, text="Wyczyść pola", command=clear_entries)
clear_button.grid(row=9, column=0, columnspan=2, pady=(5, 0))

exit_button = tk.Button(buttons_frame, text="Zamknij", command=exit_application)
exit_button.grid(row=10, column=0, columnspan=2, pady=(5, 0))

display_frame = tk.LabelFrame(root, text="Lista zadań", padx=10, pady=10)
display_frame.pack(padx=10, pady=10, fill="both", expand=True)

tasks_text = tk.Text(display_frame, height=10, width=50)
tasks_text.pack(side="left", fill="both", expand=True)

tasks_scrollbar = tk.Scrollbar(display_frame)
tasks_scrollbar.pack(side="right", fill="y")

tasks_text.config(yscrollcommand=tasks_scrollbar.set)
tasks_scrollbar.config(command=tasks_text.yview)

root.mainloop()