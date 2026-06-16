import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk

# conecta com o banco de dados
def conectar():
    conn = sqlite3.connect("db_projeto_integrador.db")
    return conn 

# função que permite apenas caracteres
def validar_texto(texto):
    return (
          all(caractere.isalpha() or caractere.isspace() for caractere in texto)
          and len(texto) <= 40
     )

def abrir_cadastro_especie(frame_especie):

    validador_nome_especie = (frame_especie.register(validar_texto), "%P")

    campo_especie_title = tk.Label(frame_especie, text="Cadastro de Espécies", font=("Times New Roman", 12, "bold"))
    campo_especie_title.pack(pady=10)

    campo_especie = tk.Entry(frame_especie, validate="key", validatecommand=validador_nome_especie)
    campo_especie.pack(pady=10)

    # cria a função que insere os valores do campo Entry no banco de dados
    def salvar():
        especie = campo_especie.get()
        if not especie:
            messagebox.showerror("Erro", "Preencha todos os campos")
            return 

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO especie (nome_especie) VALUES (?)", (especie,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Espécie cadastrada com sucesso!")
        
        # Limpa o frame depois de salvar para poder voltar à tela inicial
        for widget in frame_especie.winfo_children():
            widget.destroy()
        frame_especie.pack_forget()

    # cria o botão DENTRO do frame_pai
    tk.Button(frame_especie, text="Salvar", font=("Times New Roman", 10, "bold"), command=salvar, bg="lightgreen").pack(pady=20)