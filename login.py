import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os
 
def centralizar_janela(root, largura, altura):
 
    # Atualiza medidas
    root.update_idletasks()
 
    # Pega largura e altura da tela
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
 
    # Calcula posição X e Y
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
 
    # Define posição
    root.geometry(f"{largura}x{altura}+{x}+{y}")
 
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(diretorio_atual, "db_projeto_integrador.db")
 
def verificar_login():
    email = entry_usuario.get()
    senha = entry_senha.get()
   
    try:
       
        conn = sqlite3.connect(caminho_banco)
        cursor = conn.cursor()
       
       
        query = "SELECT * FROM usuario WHERE login = ? AND senha = ?"
        cursor.execute(query, (email, senha))
       
        resultado = cursor.fetchall()
        conn.close()
       
        if resultado:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            janela.destroy()
            subprocess.Popen(["python", "main.py"])
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")
           
    except sqlite3.OperationalError as e:
        messagebox.showerror("Erro de Banco", f"Não foi possível acessar o banco:\n{e}")
 
# Configuração da Janela
janela = tk.Tk()
janela.title("Tela de Login")
centralizar_janela(janela, 300, 185)
 
tk.Label(janela, text="Email do Usuario:", font=('bold')).pack(pady=5)
entry_usuario = tk.Entry(janela)
entry_usuario.pack()
 
tk.Label(janela, text="Senha:", font=('bold')).pack(pady=5)
entry_senha = tk.Entry(janela, show="*")
entry_senha.pack()
 
btn_login = tk.Button(janela, text="Realizar Login", bg='#90ee90', command=verificar_login)
btn_login.pack(pady=20)
 
janela.mainloop()
