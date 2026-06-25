import os
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# CORES 
COR_BG = "#f8fafc"          # Fundo da tela (Slate 50)
COR_CARD = "#ffffff"        # Fundo de containers (Branco)
COR_HEADER = "#0f172a"      # Fundo do Header (Slate 900)
COR_TEXTO_HEADER = "#ffffff" # Texto do Header
COR_TEXTO = "#1e293b"       # Texto principal (Slate 800)

# Cores 
COR_PRIMARIA = "#0ea5e9"    # Azul Moderno (Sky 500)
COR_PRIMARIA_HOVER = "#0284c7"
COR_ALERTA = "#e11d48"      # Vermelho/Rosa (Rose 600)
COR_ALERTA_HOVER = "#be123c"
COR_NEUTRO = "#e2e8f0"      # Cinza claro para botões secundários (Slate 200)
COR_NEUTRO_HOVER = "#cbd5e1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# BANCO DE DADOS
def conectar():
    caminho = os.path.join(BASE_DIR, "db_projeto_integrador.db")
    conn = sqlite3.connect(caminho, timeout=30)
    return conn

def limpar_tela(container):
    for widget in container.winfo_children():
        widget.destroy()


# COMPONENTES VISUAIS CUSTOMIZADOS
def criar_header(container, titulo):
    header = tk.Frame(container, bg=COR_HEADER, height=60)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
    
    lbl_titulo = tk.Label(
        header, text=titulo.upper(), font=("Segoe UI", 12, "bold"), 
        fg=COR_TEXTO_HEADER, bg=COR_HEADER
    )
    lbl_titulo.pack(side="left", padx=20, pady=15)
    return header

def estilizar_botao(botao, cor_padrao, cor_hover, cor_texto="white"):
    botao.configure(
        bg=cor_padrao, fg=cor_texto, relief="flat", 
        font=("Segoe UI", 10, "bold"), cursor="hand2", overrelief="flat"
    )
    botao.bind("<Enter>", lambda e: botao.configure(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.configure(bg=cor_padrao))


# CADASTRO / EDIÇÃO
def abrir_cadastro_especie(container, voltar, id_especie=None):
    limpar_tela(container)
    container.configure(bg=COR_BG)
    
    titulo = "Editar Espécie" if id_especie else "Cadastrar Espécie"
    criar_header(container, titulo)

    card = tk.Frame(container, bg=COR_CARD, highlightthickness=1, highlightbackground="#e2e8f0")
    card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=260)

    form_frame = tk.Frame(card, bg=COR_CARD)
    form_frame.pack(fill="both", expand=True, padx=35, pady=25)

    def validar_apenas_letras(texto_inserido):
        if any(char.isdigit() for char in texto_inserido):
            return False
        return True

    validador_comando = form_frame.register(validar_apenas_letras)

    # Campo de Entrada
    tk.Label(form_frame, text="Nome da Espécie",  font=("Segoe UI", 10, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(anchor="w", pady=(0, 5))

    ent_nome = tk.Entry(form_frame, font=("Segoe UI", 11), bg="#f1f5f9", fg=COR_TEXTO, relief="flat", validate="key", validatecommand=(validador_comando, "%P"))
    ent_nome.pack(fill="x", ipady=6, pady=(0, 20))

    # Modo Edição
    if id_especie:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome_especie FROM especie WHERE id_especie = ?", (id_especie,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            ent_nome.insert(0, resultado[0])

    # Salvar
    def salvar():
        nome = ent_nome.get().strip()

        if not nome:
            messagebox.showwarning("Aviso", "O nome não pode estar vazio.")
            return

        conn = conectar()
        cursor = conn.cursor()

        if id_especie:
            cursor.execute("UPDATE especie SET nome_especie = ? WHERE id_especie = ?", (nome, id_especie))
            mensagem = "Espécie atualizada com sucesso!"
        else:
            cursor.execute("INSERT INTO especie (nome_especie) VALUES (?)", (nome,))
            mensagem = "Espécie cadastrada com sucesso!"

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", mensagem)
        voltar()

    # Botões 
    frame_botoes = tk.Frame(form_frame, bg=COR_CARD)
    frame_botoes.pack(fill="x", pady=(10, 0))

    btn_voltar = tk.Button(frame_botoes, text="VOLTAR", command=voltar, width=12)
    btn_voltar.pack(side="left", ipady=6)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER, cor_texto=COR_TEXTO)

    texto_botao = "ATUALIZAR" if id_especie else "SALVAR"
    btn_salvar = tk.Button(frame_botoes, text=texto_botao, command=salvar, width=14)
    btn_salvar.pack(side="right", ipady=6)
    estilizar_botao(btn_salvar, COR_PRIMARIA, COR_PRIMARIA_HOVER)



def abrir_consulta_especie(container, voltar):
    limpar_tela(container)
    container.configure(bg=COR_BG)

    criar_header(container, "Consulta de Espécies")

    conteudo = tk.Frame(container, bg=COR_BG)
    conteudo.pack(fill="both", expand=True, padx=25, pady=20)

    # BARRA DE BUSCA
    frame_busca = tk.Frame(conteudo, bg=COR_BG)
    frame_busca.pack(fill="x", pady=(0, 15))

    tk.Label(frame_busca, text="Buscar:", font=("Segoe UI", 10, "bold"), fg=COR_TEXTO, bg=COR_BG).pack(side="left", padx=(0, 10))
    ent_busca = tk.Entry(frame_busca, font=("Segoe UI", 11), bg=COR_CARD, fg=COR_TEXTO, relief="solid", bd=1)
    ent_busca.configure(highlightbackground="#cbd5e1", highlightcolor=COR_PRIMARIA, highlightthickness=0)
    ent_busca.pack(side="left", fill="x", expand=True, ipady=4)

    # TABELA 
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", 
                    background=COR_CARD, fieldbackground=COR_CARD, 
                    foreground=COR_TEXTO, rowheight=30, font=("Segoe UI", 9), borderwidth=0)
    style.configure("Treeview.Heading", 
                    background="#e2e8f0", foreground=COR_TEXTO, 
                    font=("Segoe UI", 9, "bold"), relief="flat")
    style.map("Treeview", background=[("selected", "#e0f2fe")], foreground=[("selected", "#0369a1")])

    frame_tabela = tk.Frame(conteudo, bg=COR_BG)
    frame_tabela.pack(fill="both", expand=True)

    colunas = ("ID", "Nome da Espécie")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", style="Treeview")

    tabela.heading("ID", text="ID", anchor="center")
    tabela.heading("Nome da Espécie", text="Nome da Espécie", anchor="w")

    tabela.column("ID", width=60, anchor="center")
    tabela.column("Nome da Espécie", width=300, anchor="w")

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    tabela.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def carregar_dados(filtro=""):
        for row in tabela.get_children():
            tabela.delete(row)

        conn = conectar()
        cursor = conn.cursor()

        if filtro:
            cursor.execute("""
                SELECT id_especie, nome_especie FROM especie 
                WHERE LOWER(nome_especie) LIKE LOWER(?)
            """, ('%' + filtro + '%',))
        else:
            cursor.execute("SELECT id_especie, nome_especie FROM especie")

        for i, linha in enumerate(cursor.fetchall()):
            tag = "par" if i % 2 == 0 else "impar"
            tabela.insert("", tk.END, values=linha, tags=(tag,))
        
        tabela.tag_configure("par", background=COR_CARD)
        tabela.tag_configure("impar", background="#f8fafc")
        conn.close()

    ent_busca.bind("<KeyRelease>", lambda e: carregar_dados(ent_busca.get()))

    # Edição
    def executar_edicao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma espécie para editar!")
            return

        id_especie = tabela.item(item, "values")[0]
        abrir_cadastro_especie(container, lambda: abrir_consulta_especie(container, voltar), id_especie=id_especie)

    def executar_exclusao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma espécie para excluir!")
            return

        valores = tabela.item(item, "values")
        id_especie, nome = valores[0], valores[1]

        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir '{nome}'?"):
            conn = conectar()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM especie WHERE id_especie = ?", (id_especie,))
                conn.commit()
                messagebox.showinfo("Sucesso", "Espécie excluída com sucesso!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Não é possível excluir: existem raças vinculadas a esta espécie.")
            
            conn.close()
            carregar_dados()

    # Rodapé 
    frame_botoes = tk.Frame(conteudo, bg=COR_BG)
    frame_botoes.pack(fill="x", pady=(15, 0))

    btn_voltar = tk.Button(frame_botoes, text="VOLTAR", command=voltar, width=12)
    btn_voltar.pack(side="left", ipady=6)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER, cor_texto=COR_TEXTO)

    btn_excluir = tk.Button(frame_botoes, text="EXCLUIR", command=executar_exclusao, bg=COR_ALERTA, width=12)
    btn_excluir.pack(side="right", ipady=6, padx=(10, 0))
    estilizar_botao(btn_excluir, COR_ALERTA, COR_ALERTA_HOVER)

    btn_editar = tk.Button(frame_botoes, text="EDITAR", command=executar_edicao, width=12)
    btn_editar.pack(side="right", ipady=6)
    estilizar_botao(btn_editar, COR_PRIMARIA, COR_PRIMARIA_HOVER)

    carregar_dados()