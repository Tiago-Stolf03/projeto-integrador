import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

def __init__(self, id_usuario, login, senha):
        self.id_usuario = id_usuario
        self.login = login
        self.senha = senha

def cadastrar(self):
        conn = sqlite3.connect("./projeto_integrador/db_projeto_integrador.db")
        cursor = conn.cursor()
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS "usuario" ( "id_usuario" INTEGER, "login" VARCHAR(50) NOT NULL, "senha" VARCHAR(50) NOT NULL, PRIMARY KEY("id_usuario" AUTOINCREMENT) );
        ''')
        cursor.execute('''
            INSERT INTO usuarios (id_usuario, login, senha) VALUES (?, ?, ?)
        ''', (self.id_usuario, self.login, self.senha))
        conn.commit()
        conn.close()

def cadastrar_usuario(id_usuario, login, senha):
    execution = False

    if not login or not senha:
        messagebox.showwarning("Atenção", "Login e senha são obrigatórios!")
        return execution
    
    try:
        conn = sqlite3.connect('db_projeto_integrador.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "usuario" ( "id_usuario" INTEGER, "login" VARCHAR(50) NOT NULL, "senha" VARCHAR(50) NOT NULL, PRIMARY KEY("id_usuario" AUTOINCREMENT) );
        ''')
        cursor.execute('''
            INSERT INTO usuario (id_usuario, login, senha) VALUES (?, ?, ?)
        ''', (id_usuario, login, senha))
        conn.commit()
        execution = True
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar o usuário: {e}")
    finally:
        conn.close()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    return execution

root = tk.Tk()
root.title("Cadastro de Usuário")

tk.Label(root, text="Login:").pack()
login_entry = tk.Entry(root)
login_entry.pack()

tk.Label(root, text="Senha:").pack()
senha_entry = tk.Entry(root, show="*")
senha_entry.pack()

tk.Button(root, text="Cadastrar", command=lambda: cadastrar_usuario(None, login_entry.get(), senha_entry.get())).pack()

root.geometry("400x500")
root.mainloop()