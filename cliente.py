import sqlite3
import os
import tkinter as tk
from tkinter import ttk, messagebox

def conectar():
    """Conecta ao banco de dados que está na mesma pasta do arquivo .py"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "db_projeto_integrador.db")
    return sqlite3.connect(db_path)

def formatar_cpf(event):
    entry = event.widget
    texto = entry.get()
    texto = "".join(filter(str.isdigit, texto))
    texto = texto[:11]
    novo = ""


    if len(texto) >= 1:
        novo += texto[:3]
    if len(texto) >= 4:
        novo += "." + texto[3:6]
    if len(texto) >= 7:
        novo += "." + texto[6:9]
    if len(texto) >= 10:
        novo += "-" + texto[9:11]


    entry.delete(0, tk.END)
    entry.insert(0, novo)


# =========================
# FORMATAÇÃO TELEFONE
# =========================


def formatar_telefone(event):
    entry = event.widget
    texto = entry.get()
    texto = "".join(filter(str.isdigit, texto))
    texto = texto[:11]
    novo = ""


    if len(texto) >= 1:
        novo += "(" + texto[:2]
    if len(texto) >= 3:
        novo += ") " + texto[2:7]
    if len(texto) >= 8:
        novo += "-" + texto[7:11]


    entry.delete(0, tk.END)
    entry.insert(0, novo)

root = tk.Tk()
root.title("Cadastro de Cliente")
root.geometry("400x420")

tk.Label(root, text="Cadastro de Cliente", font=("Arial", 16, "bold")).pack(pady=15)

tk.Label(root, text="Nome do Cliente (Coloque sobrenome!):", font=("Arial", 10)).pack(pady=15)
nome_cliente_entry = tk.Entry(root, width=40)
nome_cliente_entry.pack(pady=3)

tk.Label(root, text="CPF:").pack()
ent_cpf = tk.Entry(root, width=40)
ent_cpf.pack(pady=5)
ent_cpf.bind("<KeyRelease>", formatar_cpf)


tk.Label(root, text="Endereço:").pack()
endereco_entry = tk.Entry(root, width=40)
endereco_entry.pack(pady=3)

tk.Label(root, text="Telefone:").pack()
ent_telefone = tk.Entry(root, width=40)
ent_telefone.pack(pady=5)
ent_telefone.bind("<KeyRelease>", formatar_telefone)



def cadastrar():
    nome_cliente = nome_cliente_entry.get()
    cpf = ent_cpf.get()
    endereco = endereco_entry.get()
    telefone = ent_telefone.get()

    if not nome_cliente:
        messagebox.showwarning("Atenção", "O nome do cliente é obrigatório!")
        return
    if not cpf:
        messagebox.showwarning("Atenção", "O CPF é obrigatório!")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cliente (nome_cliente, cpf, endereco, telefone) 
            VALUES (?, ?, ?, ?)
        """, (nome_cliente, cpf, endereco, telefone))
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        root.destroy()
        
    except sqlite3.IntegrityError:
        messagebox.showerror("Erro", "Este CPF já está cadastrado!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar cliente:\n{str(e)}")

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=25)

ttk.Button(frame_botoes, text="Cadastrar", command=cadastrar, width=15).pack(side=tk.LEFT, padx=10)
ttk.Button(frame_botoes, text="Cancelar", command=root.destroy, width=15).pack(side=tk.LEFT, padx=10)

