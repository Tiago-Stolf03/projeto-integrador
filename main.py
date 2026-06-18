import tkinter as tk
from tkinter import messagebox
import sqlite3
import add_especie
import add_raca
import cliente_v2

# ---------------------------------------------------------------------------------------------------------------------------------
# tela principal
main_tela = tk.Tk()
main_tela.title("Início")
main_tela.geometry("600x500")

# titulo da tela
nome_principal = tk.Label(main_tela,text="PET MATCH",font=("Times New Roman",14,"bold"))
nome_principal.pack(anchor="center")

# frame da tela principal
frame_main = tk.Frame(main_tela)
# --------------------------------------------------------------------------------------------------------------------
def voltar_menu():
    # Remove todos os widgets que foram adicionados ao frame
    for widget in frame_main.winfo_children():
        widget.destroy()

    frame_main.pack_forget()

    # Mostra novamente os botões do menu principal
    botao_cliente.place(rely=0.15, relx=0.5, anchor="center")
    botao_raca.place(rely=0.30, relx=0.5, anchor="center")
    botao_especie.place(rely=0.45, relx=0.5, anchor="center")
# ---------------------------------------------------------------------------------------------------------------------
# botão cadastro espécie
botao_especie = tk.Button( main_tela, padx=10, pady=10, text="Adicionar Espécie", 
    command=lambda: [ 
        botao_especie.place_forget(), botao_raca.place_forget(), botao_cliente.place_forget(), botao_sair.place_forget(),
    frame_main.pack(fill="both", expand=True),  
    add_especie.abrir_cadastro_especie(frame_main, voltar_menu) ]  )

botao_especie.place(rely=0.45,relx=0.5, anchor="center")

# botão cadastro raça
botao_raca = tk.Button( main_tela, padx=10, pady=10, text="Adicionar Raça", 
    command=lambda: [ 
        botao_raca.place_forget(), botao_especie.place_forget(), botao_cliente.place_forget(), botao_sair.place_forget(),
    frame_main.pack(fill="both", expand=True),  
    add_raca.abrir_cadastro_raca(frame_main, voltar_menu) ]  )

botao_raca.place(rely=0.3,relx=0.5, anchor="center")

# botão cadastro cliente
botao_cliente = tk.Button( main_tela, padx=10, pady=10, text="Cadastrar Cliente",
    command=lambda: [ 
        botao_raca.place_forget(), botao_especie.place_forget(), botao_cliente.place_forget(), botao_sair.place_forget(),
    frame_main.pack(fill="both", expand=True),  
    cliente_v2.abrir_cadastro_cliente(frame_main, voltar_menu) ]  )

botao_cliente.place(rely=0.15, relx=0.5, anchor="center")


botao_sair = tk.Button( main_tela, bg="firebrick", text="SAIR", pady=10, padx=30, command=lambda:main_tela.destroy())
botao_sair.place(rely=0.75, relx=0.5, anchor="center")

main_tela.mainloop()
# --------------------------------------------------------------------------------------------------------------------------------------------------