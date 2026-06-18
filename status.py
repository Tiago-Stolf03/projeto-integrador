import sqlite3
import os
import tkinter as tk
from tkinter import ttk, messagebox

def conectar():
    """Conecta ao banco de dados na mesma pasta do arquivo .py"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "db_projeto_integrador.db")
    return sqlite3.connect(db_path)

def cadastrar_status(nome_status):
    """Cadastra um novo status no banco de dados"""
    if not nome_status or not nome_status.strip():
        messagebox.showwarning("Atenção", "O nome do status é obrigatório!")
        return False

    nome_status = nome_status.strip()

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS status (
                id_status INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_status VARCHAR(50) NOT NULL
            )
        ''')

        cursor.execute('''
            INSERT INTO status (nome_status) VALUES (?)
        ''', (nome_status,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", f"Status '{nome_status}' cadastrado com sucesso!")
        return True

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar o status:\n{e}")
        return False

root = tk.Tk()
root.title("Cadastro de Status")
root.geometry("400x250")

tk.Label(root, text="Cadastro de Status", font=("Arial", 16, "bold")).pack(pady=20)

tk.Label(root, text="Nome do Status:").pack()
nome_status_entry = tk.Entry(root, width=40)
nome_status_entry.pack(pady=10)

def acao_cadastrar():
    nome = nome_status_entry.get()
    if cadastrar_status(nome):
        nome_status_entry.delete(0, tk.END)

ttk.Button(root, text="Cadastrar Status", command=acao_cadastrar, width=20).pack(pady=15)

root.mainloop()