import sqlite3
import tkinter as tk
import tkinter as messagebox

def __init__(self, id_usuario, login, senha):
        self.id_usuario = id_usuario
        self.login = login
        self.senha = senha

def guardar_en_db(self):
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('''
           CREATE TABLE "usuario" ( "id_usuario" INTEGER, "login" VARCHAR(50) NOT NULL, "senha" VARCHAR(50) NOT NULL, PRIMARY KEY("id_usuario" AUTOINCREMENT) );
        ''')
        cursor.execute('''
            INSERT INTO usuarios (id_usuario, login, senha) VALUES (?, ?, ?)
        ''', (self.id_usuario, self.login, self.senha))
        conn.commit()
        conn.close()

