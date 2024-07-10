import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='parola',  # Introdu parola ta MySQL
            database='hotel'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        messagebox.showerror("Connection Error", str(e))
        return None

def fetch_data():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM camere")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_data(row_id, nr_camera, etaj, pret):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE camere
            SET NrCamera = %s, Etaj = %s, Pret = %s
            WHERE IdCamera = %s
        """, (nr_camera, etaj, pret, row_id))
        conn.commit()
        conn.close()
    except Error as e:
        messagebox.showerror("Update Error", str(e))

def insert_data(nr_camera, etaj, pret):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO camere (NrCamera, Etaj, Pret)
            VALUES (%s, %s, %s)
        """, (nr_camera, etaj, pret))
        conn.commit()
        conn.close()
    except Error as e:
        messagebox.showerror("Insert Error", str(e))

def delete_data(row_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM camere WHERE IdCamera = %s", (row_id,))
        conn.commit()
        conn.close()
    except Error as e:
        messagebox.showerror("Delete Error", str(e))

def on_update():
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, 'values')
    update_window = tk.Toplevel(root)
    update_window.title("Update Camera")

    tk.Label(update_window, text="Nr. Camera").grid(row=0, column=0)
    nr_camera_entry = tk.Entry(update_window)
    nr_camera_entry.grid(row=0, column=1)
    nr_camera_entry.insert(0, values[1])

    tk.Label(update_window, text="Etaj").grid(row=1, column=0)
    etaj_entry = tk.Entry(update_window)
    etaj_entry.grid(row=1, column=1)
    etaj_entry.insert(0, values[2])

    tk.Label(update_window, text="Pret").grid(row=2, column=0)
    pret_entry = tk.Entry(update_window)
    pret_entry.grid(row=2, column=1)
    pret_entry.insert(0, values[3])

    def save_changes():
        update_data(values[0], nr_camera_entry.get(), etaj_entry.get(), pret_entry.get())
        update_window.destroy()
        refresh_data()

    tk.Button(update_window, text="Save", command=save_changes).grid(row=3, columnspan=2)

def on_add():
    add_window = tk.Toplevel(root)
    add_window.title("Add Camera")

    tk.Label(add_window, text="Nr. Camera").grid(row=0, column=0)
    nr_camera_entry = tk.Entry(add_window)
    nr_camera_entry.grid(row=0, column=1)

    tk.Label(add_window, text="Etaj").grid(row=1, column=0)
    etaj_entry = tk.Entry(add_window)
    etaj_entry.grid(row=1, column=1)

    tk.Label(add_window, text="Pret").grid(row=2, column=0)
    pret_entry = tk.Entry(add_window)
    pret_entry.grid(row=2, column=1)

    def add_camera():
        insert_data(nr_camera_entry.get(), etaj_entry.get(), pret_entry.get())
        add_window.destroy()
        refresh_data()

    tk.Button(add_window, text="Add", command=add_camera).grid(row=3, columnspan=2)

def on_delete():
    selected_item = tree.selection()[0]
    values = tree.item(selected_item, 'values')
    delete_data(values[0])
    refresh_data()

def refresh_data():
    for i in tree.get_children():
        tree.delete(i)
    rows = fetch_data()
    for row in rows:
        tree.insert('', 'end', values=row)

root = tk.Tk()
root.title("Hotel Management")

tree = ttk.Treeview(root, columns=("IdCamera", "NrCamera", "Etaj", "Pret"), show='headings')
tree.heading("IdCamera", text="ID Camera")
tree.heading("NrCamera", text="Nr. Camera")
tree.heading("Etaj", text="Etaj")
tree.heading("Pret", text="Pret")
tree.pack()

refresh_data()

btn_frame = tk.Frame(root)
btn_frame.pack()

btn_update = tk.Button(btn_frame, text="Update", command=on_update)
btn_update.grid(row=0, column=0)

btn_add = tk.Button(btn_frame, text="Add", command=on_add)
btn_add.grid(row=0, column=1)

btn_delete = tk.Button(btn_frame, text="Delete", command=on_delete)
btn_delete.grid(row=0, column=2)

root.mainloop()
