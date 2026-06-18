import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk

# conecta com o banco de dados
def conectar():
    conn = sqlite3.connect("./projeto-integrador/db_projeto_integrador.db")
    cursor = conn.cursor()
    conn.commit()
    return conn

# cria a função que permite apenas caracteres
def validar_texto(texto):
    return (
          all(caractere.isalpha() or caractere.isspace() for caractere in texto)
          and len(texto) <= 40
     )

def abrir_cadastro_especie():

    # cria a tela principal da tabela especie
    janela_especie = tk.Tk()
    janela_especie.title = ("Tela Espécies")
    janela_especie.geometry("350x350")
    janela_especie.configure()

    # registra a funcao validar texto na janela_especie
    validador_nome_especie = (janela_especie.register(validar_texto), "%P")

    # cria o titulo 
    campo_especie_title = tk.Label(janela_especie, text= "Cadastro de Espécies", font=("Times New Roman",12,"bold"))
    campo_especie_title.pack(pady=10)

    # cria o entry e valida para permitir apenas letras
    campo_especie = tk.Entry(janela_especie, validate="key", validatecommand=validador_nome_especie)
    campo_especie.pack(pady=10)

    # cria a função que insere os valores do campo Entry no banco de dados
    def salvar():
        especie = campo_especie.get()
        if not especie:
            messagebox.showerror("Erro","Preencha todos os campos")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO especie (nome_especie) VALUES (?)", (especie,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Espécie cadastrada com sucesso!")
        janela_especie.destroy()

    # cria o botão que envia as informações digitadas para o banco de dados
    tk.Button(janela_especie, text="Salvar",font=("Times New Roman",10,"bold"), command=salvar, bg="lightgreen").pack(pady=20)

    janela_especie.mainloop()

abrir_cadastro_especie()

    

