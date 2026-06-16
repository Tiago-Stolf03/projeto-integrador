import tkinter as tk
from tkinter import messagebox
import sqlite3
import add_especie
import add_raca

main_tela = tk.Tk()
main_tela.title("Início")
main_tela.geometry("600x500")

nome_principal = tk.Label(main_tela,text="PET MATCH",font=("Times New Roman",14,"bold"))
nome_principal.pack(anchor="center")

frame_especie_main = tk.Frame(main_tela)

botao_especie = tk.Button(
    main_tela, padx=10, pady=10, 
    text="Adicionar Espécie", 
    command=lambda: [
        botao_especie.place_forget(), 
        frame_especie_main.pack(fill="both", expand=True), 
        add_especie.abrir_cadastro_especie(frame_especie_main)
    ]
)
botao_especie.place(rely=0.5,relx=0.5, anchor="center")


botao_raca = tk.Button(
    main_tela, padx=10, pady=10, 
    text="Adicionar Raça", 
    command=lambda: [
        botao_raca.place_forget(), 
        frame_especie_main.pack(fill="both", expand=True), 
        add_raca.abrir_cadastro_raca(frame_especie_main)
    ]
)
botao_raca.place(rely=0.3,relx=0.5, anchor="center")

main_tela.mainloop()