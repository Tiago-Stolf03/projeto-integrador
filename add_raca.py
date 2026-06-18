import tkinter as tk
import sqlite3
from tkinter import messagebox, ttk

# conecta com o banco de dados
def conectar():
    conn = sqlite3.connect("db_projeto_integrador.db")
    return conn

# busca tudo da tabela especie
def buscar_especies():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM especie")
    dados = cursor.fetchall()
    conn.close()
    return dados

# cria a função que permite apenas caracteres
def validar_texto(texto):
    return (
          all(caractere.isalpha() or caractere.isspace() for caractere in texto)
          and len(texto) <= 40
     )
# -------------------------------------------------------------------------------------------------------------------------------------------
def abrir_cadastro_raca(frame_raca, voltar_menu):
    lista_especies = buscar_especies()
    nome_especies = [esp[1] for esp in lista_especies]
    id_especies = {esp[1]: esp[0] for esp in lista_especies}

    # faz a ligação entre os campos nome_especie e id_especie, dessa forma, quando selecionar o nome da espécie ele vai automaticamente buscar o id dela no bd
    def pegar_id(event):
        especieID =  campo_especie.get()

        if especieID in id_especies:
            return campo_id_especie.config(text=f"{id_especies[especieID]}")

    # registra a funcao validar texto na janela_especie
    validador_nome_raca = (frame_raca.register(validar_texto), "%P")
# ---------------------------------------------------------------------------------------------------------------------
    # cria o titulo 
    titulo_janela = tk.Label(frame_raca, text= "Cadastro de Raças", font=("Times New Roman",12,"bold"))
    titulo_janela.pack(pady=30)
# --------------------------------------------------------------------------------------------------------------------
    campo_especie_title = tk.Label(frame_raca, text= "Selecione uma Espécie", font=("Times New Roman",12))
    campo_especie_title.pack()

    # o .bind faz a ligação desse Combobox com a função pegar_id
    campo_especie = ttk.Combobox(frame_raca, values=nome_especies, state="readonly")
    campo_especie.pack()
    campo_especie.bind("<<ComboboxSelected>>", pegar_id)

    campo_id_especie = tk.Label(frame_raca, text="")
    campo_id_especie.pack(pady=15)
# --------------------------------------------------------------------------------------------------------------------
    campo_raca_title = tk.Label(frame_raca, text= "Digite uma Raça", font=("Times New Roman",12))
    campo_raca_title.pack()

    campo_raca = tk.Entry(frame_raca, validate="key", validatecommand=validador_nome_raca)
    campo_raca.pack(pady=10)
# ---------------------------------------------------------------------------------------------------------------------
    # cria a função que insere os valores do campo Entry no banco de dados
    def salvar():
        id_da_especie = campo_id_especie.cget("text")
        raca = campo_raca.get()

        if not id_da_especie:
            messagebox.showerror("Erro","Preencha todos os campos")
        if not raca:
            messagebox.showerror("Erro","Preencha todos os campos")

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO raca (id_especie, nome_raca ) VALUES (?, ?)", (id_da_especie, raca,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Espécie cadastrada com sucesso!")

    # cria o botão que envia as informações digitadas para o banco de dados
    tk.Button(frame_raca, text="Salvar",font=("Times New Roman",12,"bold"), command=salvar, bg="lightgreen").pack(pady=20)

    voltar_button = tk.Button(frame_raca, text="Voltar", bg="crimson" ,font=("Times New Roman", 14, "bold"),command=voltar_menu)
    voltar_button.pack(pady=10)
   