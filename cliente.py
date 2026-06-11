import sqlite3
import tkinter as tk
import tkinter as messagebox

def cadastrar_cliente(id_cliente, nome_cliente, cpf, endereco, telefone):
    execution = False
    try:
        conn = sqlite3.connect('clientes.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE "cliente" ( "id_cliente" INTEGER, "nome_cliente" VARCHAR(50) NOT NULL, "cpf" VARCHAR(50) NOT NULL UNIQUE, "endereco" VARCHAR(50) NOT NULL, "telefone" VARCHAR(50) NOT NULL, PRIMARY KEY("id_cliente" AUTOINCREMENT) );
        ''')
        cursor.execute('''
            INSERT INTO clientes (id_cliente, nome_cliente, cpf, endereco, telefone) VALUES (?, ?, ?, ?, ?)
        ''', (id_cliente, nome_cliente, cpf, endereco, telefone))
        conn.commit()
        execution = True
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao cadastrar o cliente: {e}")
    finally:
        conn.close()
    return execution