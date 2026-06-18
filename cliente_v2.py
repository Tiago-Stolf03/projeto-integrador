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
def validar_numero(numero):
     return(
          all(num.isdigit() for num in numero)
          and len(numero) <= 11
     )

def abrir_cadastro_cliente(frame_cliente, voltar_menu):

    validador_nome_cliente = (frame_cliente.register(validar_texto), "%P")
    validador_CPF_telefone = (frame_cliente.register(validar_numero), "%P")
# ----------------------------------------------------------------------------------------------------------- criação de todos os textos e campos digitáveis

    titulo_cliente = tk.Label(frame_cliente,text="Cadastro de Clientes",font=("Times New Roman", 12, "bold"))
    titulo_cliente.pack(pady=10)
# ---------------------------------------------------------------------------------------------
    campo1_tittle = tk.Label(frame_cliente,text="Nome Cliente", font=("Times New Roman",12))
    campo1_tittle.pack()

    campo_cliente_nome = tk.Entry(frame_cliente, validate="key", validatecommand=validador_nome_cliente)
    campo_cliente_nome.pack(pady=10)
# ----------------------------------------------------------------------------------------------
    campo2_tittle = tk.Label(frame_cliente,text="CPF", font=("Times New Roman",12))
    campo2_tittle.pack()

    campo_cliente_CPF = tk.Entry(frame_cliente, validate="key", validatecommand=validador_CPF_telefone)
    campo_cliente_CPF.pack(pady=10)
# ----------------------------------------------------------------------------------------------
    campo3_tittle = tk.Label(frame_cliente,text="Endereço", font=("Times New Roman",12))
    campo3_tittle.pack()

    campo_cliente_endereco = tk.Entry(frame_cliente)
    campo_cliente_endereco.pack(pady=10)
# ----------------------------------------------------------------------------------------------
    campo4_tittle = tk.Label(frame_cliente,text="Telefone", font=("Times New Roman",12))
    campo4_tittle.pack()

    campo_cliente_telefone = tk.Entry(frame_cliente, validate="key", validatecommand=validador_CPF_telefone)
    campo_cliente_telefone.pack(pady=10)
# ----------------------------------------------------------------------------------------------------------- aqui finaliza a criação dos campos
# insere no banco de dados os valores digitados
    def salvar():
        nome_cliente = campo_cliente_nome.get()
        cpf = campo_cliente_CPF.get()
        endereco = campo_cliente_endereco.get()
        telefone = campo_cliente_telefone.get()

        if not nome_cliente:
            messagebox.showwarning("Aviso","Preencha todos os campos")
        if not cpf:
            messagebox.showwarning("Aviso","Preencha todos os campos")
        if not endereco:
            messagebox.showwarning("Aviso","Preencha todos os campos")
        if not telefone:
            messagebox.showwarning("Aviso","Preencha todos os campos")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cliente (nome_cliente, cpf, endereco, telefone) VALUES (?, ?, ?, ?)", (nome_cliente, cpf, endereco, telefone,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

    tk.Button(frame_cliente, text="Salvar", font=("Times New Roman", 12, "bold"), command=salvar, bg="lightgreen").pack(pady=20)
        
    voltar_button = tk.Button(frame_cliente, text="Voltar", bg="crimson" ,font=("Times New Roman", 14, "bold"),command=voltar_menu)
    voltar_button.pack(pady=10)