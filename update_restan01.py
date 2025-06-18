import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import schedule
import time
import threading

def call_procedure(db_host, db_user, db_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()
        cursor.execute("CALL updateRestan01(NULL, NULL);")
        connection.commit()
        messagebox.showinfo("Success", f"[{datetime.now()}] Prosedur berhasil dijalankan.")
    except Exception as e:
        messagebox.showerror("Error", f"[{datetime.now()}] ERROR: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def run_schedule(db_host, db_user, db_password, db_name):
    schedule.every(20).minutes.do(lambda: call_procedure(db_host, db_user, db_password, db_name))
    while True:
        schedule.run_pending()
        time.sleep(60)

def start_connection():
    db_host = entry_host.get()
    db_user = entry_user.get()
    db_password = entry_password.get()
    db_name = entry_dbname.get()

    if not db_host or not db_user or not db_password or not db_name:
        messagebox.showwarning("Input Error", "Semua kolom harus diisi!")
        return
   
    threading.Thread(target=run_schedule, args=(db_host, db_user, db_password, db_name), daemon=True).start()
    messagebox.showinfo("Started", "Proses berjalan di latar belakang, menunggu jadwal...")

root = tk.Tk()
root.title("Database Connection")

label_host = tk.Label(root, text="DB_HOST :")
label_host.grid(row=0, column=0, padx=10, pady=5)
entry_host = tk.Entry(root)
entry_host.grid(row=0, column=1, padx=10, pady=5)

label_user = tk.Label(root, text="DB_USER:")
label_user.grid(row=1, column=0, padx=10, pady=5)
entry_user = tk.Entry(root)
entry_user.grid(row=1, column=1, padx=10, pady=5)

label_password = tk.Label(root, text="DB_PASSWORD:")
label_password.grid(row=2, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=2, column=1, padx=10, pady=5)

label_dbname = tk.Label(root, text="DB_NAME:")
label_dbname.grid(row=3, column=0, padx=10, pady=5)
entry_dbname = tk.Entry(root)
entry_dbname.grid(row=3, column=1, padx=10, pady=5)

start_button = tk.Button(root, text="Start Connection", command=start_connection)
start_button.grid(row=4, columnspan=2, pady=20)

root.mainloop()
