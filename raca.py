import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os


# CORES 

COR_BG = "#f8fafc"          # Fundo da tela (Slate 50)
COR_CARD = "#ffffff"        # Fundo de containers (Branco)
COR_HEADER = "#0f172a"      # Fundo do Header (Slate 900)
COR_TEXTO_HEADER = "#ffffff" # Texto do Header
COR_TEXTO = "#1e293b"       # Texto principal (Slate 800)
COR_MUTED = "#64748b"       # Texto secundário (Slate 500)

# Cores
COR_PRIMARIA = "#0ea5e9"    # Azul Moderno (Sky 500)
COR_PRIMARIA_HOVER = "#0284c7"
COR_ALERTA = "#e11d48"      # Vermelho/Rosa (Rose 600)
COR_ALERTA_HOVER = "#be123c"
COR_NEUTRO = "#e2e8f0"      # Cinza claro para botões secundários (Slate 200)
COR_NEUTRO_HOVER = "#cbd5e1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def conectar():
    conn = sqlite3.connect(os.path.join(BASE_DIR, "db_projeto_integrador.db"), timeout=30)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raca (
            id_raca INTEGER PRIMARY KEY AUTOINCREMENT,
            id_especie INTEGER NOT NULL,
            nome_raca VARCHAR(50) NOT NULL,
            FOREIGN KEY(id_especie) REFERENCES especie(id_especie)
        )
    """)
    conn.commit()
    return conn

def limpar_tela(container):
    for widget in container.winfo_children():
        widget.destroy()

def obter_especies():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_especie, nome_especie FROM especie")
        dados = cursor.fetchall()
    except sqlite3.OperationalError:
        # Fallback caso a tabela espécie ainda não exista no teste do usuário
        dados = [(1, "Cachorro"), (2, "Gato")]
    conn.close()
    return dados


def criar_header(container, titulo):
    """Cria um cabeçalho moderno e destacado para a tela"""
    header = tk.Frame(container, bg=COR_HEADER, height=60)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
    
    lbl_titulo = tk.Label(
        header, text=titulo.upper(), font=("Segoe UI", 14, "bold"), 
        fg=COR_TEXTO_HEADER, bg=COR_HEADER
    )
    lbl_titulo.pack(side="left", padx=20, pady=15)
    return header

def estilizar_botao(botao, cor_padrao, cor_hover):
    """Aplica o efeito hover e estilo flat aos botões"""
    botao.configure(
        relief="flat", font=("Segoe UI", 10, "bold"), 
        cursor="hand2", overrelief="flat"
    )
    botao.bind("<Enter>", lambda e: botao.configure(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.configure(bg=cor_padrao))


# CADASTRO / EDIÇÃO DE RAÇA
def abrir_cadastro_raca(container, voltar, id_raca=None):
    limpar_tela(container)
    container.configure(bg=COR_BG)
    
    titulo = "Editar Raça" if id_raca else "Cadastrar Raça"
    criar_header(container, titulo)

    # Card centralizado 
    card = tk.Frame(container, bg=COR_CARD, bd=1, relief="solid", highlightthickness=0, colormap="new")
    # Simula uma borda suave alterando a cor de fundo do frame externo ou usando propriedades nativas
    card.configure(highlightbackground="#e2e8f0", highlightcolor="#e2e8f0", bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=450, height=320)

    
    form_frame = tk.Frame(card, bg=COR_CARD)
    form_frame.pack(fill="both", expand=True, padx=30, pady=25)

    # Validador letras
    def validar_apenas_letras(texto_inserido):
        return all(char.isalpha() or char.isspace() for char in texto_inserido)

    validador_comando = form_frame.register(validar_apenas_letras)

    # Campo: Nome da Raça
    tk.Label(form_frame, text="Nome da Raça", font=("Segoe UI", 10, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(anchor="w", pady=(0, 5))
    ent_nome_raca = tk.Entry(
        form_frame, font=("Segoe UI", 11), bg="#f1f5f9", fg=COR_TEXTO,
        relief="flat", insertbackground=COR_TEXTO, validate="key", 
        validatecommand=(validador_comando, "%P")
    )
    ent_nome_raca.pack(fill="x", ipady=6, pady=(0, 15))
    
    # Campo: Espécie
    lista_especie = obter_especies()
    nomes_especie = [e[1] for e in lista_especie]

    tk.Label(form_frame, text="Espécie Pertencente", font=("Segoe UI", 10, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(anchor="w", pady=(0, 5))
    
    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", fieldbackground="#f1f5f9", background="#e2e8f0", arrowcolor=COR_TEXTO, borderwidth=0)
    
    combo_especie = ttk.Combobox(
        form_frame, values=nomes_especie, font=("Segoe UI", 10), state="readonly", style="TCombobox"
    )
    combo_especie.pack(fill="x", ipady=4, pady=(0, 25))

    # Carregar Dados se for Edição
    if id_raca:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome_raca, id_especie FROM raca WHERE id_raca = ?", (id_raca,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            nome_raca, id_esp = resultado
            ent_nome_raca.insert(0, nome_raca)
            ids_esp = [e[0] for e in lista_especie]
            if id_esp in ids_esp:
                combo_especie.current(ids_esp.index(id_esp))

    # Lógica Salvar
    def salvar():
        nome = ent_nome_raca.get().strip()
        idx_esp = combo_especie.current()

        if not nome:
            messagebox.showwarning("Aviso", "O nome da raça não pode ficar vazio.")
            return

        if idx_esp == -1:
            messagebox.showwarning("Aviso", "Selecione uma espécie para esta raça.")
            return

        id_especie = lista_especie[idx_esp][0]
        conn = conectar()
        cursor = conn.cursor()

        if id_raca:
            cursor.execute("UPDATE raca SET nome_raca = ?, id_especie = ? WHERE id_raca = ?", (nome, id_especie, id_raca))
            mensagem = "Raça atualizada com sucesso!"
        else:
            cursor.execute("INSERT INTO raca (nome_raca, id_especie) VALUES (?, ?)", (nome, id_especie))
            mensagem = "Raça cadastrada com sucesso!"

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", mensagem)
        voltar()

    # Botões 
    frame_botoes = tk.Frame(form_frame, bg=COR_CARD)
    frame_botoes.pack(fill="x", side="bottom")

    btn_voltar = tk.Button(frame_botoes, text="VOLTAR", bg=COR_NEUTRO, fg=COR_TEXTO, width=12)
    btn_voltar.configure(command=voltar)
    btn_voltar.pack(side="left", ipady=6)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER)

    texto_botao = "ATUALIZAR" if id_raca else "SALVAR RAÇA"
    btn_salvar = tk.Button(frame_botoes, text=texto_botao, bg=COR_PRIMARIA, fg="white", width=16)
    btn_salvar.configure(command=salvar)
    btn_salvar.pack(side="right", ipady=6)
    estilizar_botao(btn_salvar, COR_PRIMARIA, COR_PRIMARIA_HOVER)



# CONSULTA DE RAÇAS
def abrir_consulta_raca(container, voltar):
    limpar_tela(container)
    container.configure(bg=COR_BG)

    criar_header(container, "Consulta de Raças")

    # Área de Conteúdo principal (com margens)
    conteudo = tk.Frame(container, bg=COR_BG)
    conteudo.pack(fill="both", expand=True, padx=30, pady=20)

    # BARRA DE BUSCA
    frame_busca = tk.Frame(conteudo, bg=COR_BG)
    frame_busca.pack(fill="x", pady=(0, 15))

    tk.Label(frame_busca, text="Buscar Raça:", font=("Segoe UI", 10, "bold"), fg=COR_TEXTO, bg=COR_BG).pack(side="left", padx=(0, 10))
    ent_busca = tk.Entry(frame_busca, font=("Segoe UI", 11), bg=COR_CARD, fg=COR_TEXTO, relief="solid", bd=1, highlightthickness=0)
    # Define uma borda cinza bem leve nativa para o input de busca
    ent_busca.configure(highlightbackground="#cbd5e1", highlightcolor=COR_PRIMARIA)
    ent_busca.pack(side="left", fill="x", expand=True, ipady=4)

    # CUSTOMIZAÇÃO DA TABELA (TREEVIEW)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", 
                    background=COR_CARD, fieldbackground=COR_CARD, 
                    foreground=COR_TEXTO, rowheight=30, font=("Segoe UI", 10), borderwidth=0)
    style.configure("Treeview.Heading", 
                    background="#e2e8f0", foreground=COR_TEXTO, 
                    font=("Segoe UI", 10, "bold"), relief="flat")
    style.map("Treeview", background=[("selected", "#e0f2fe")], foreground=[("selected", "#0369a1")])

    # Criando o container da Tabela
    frame_tabela = tk.Frame(conteudo, bg=COR_BG)
    frame_tabela.pack(fill="both", expand=True)

    colunas = ("ID", "Raça", "Espécie")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", style="Treeview")

    for coluna in colunas:
        tabela.heading(coluna, text=coluna, anchor="w" if coluna != "ID" else "center")

    tabela.column("ID", width=80, anchor="center", minwidth=50)
    tabela.column("Raça", width=250, anchor="w")
    tabela.column("Espécie", width=250, anchor="w")
    
   
    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    
    tabela.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # CARREGAR DADOS
    def carregar_dados(filtro=""):
        for row in tabela.get_children():
            tabela.delete(row)

        conn = conectar()
        cursor = conn.cursor()

        query_base = """
        SELECT r.id_raca, r.nome_raca, e.nome_especie
        FROM raca r
        LEFT JOIN especie e ON r.id_especie = e.id_especie
        """
        if filtro:
            cursor.execute(query_base + " WHERE LOWER(r.nome_raca) LIKE LOWER(?)", ('%' + filtro + '%',))
        else:
            cursor.execute(query_base)

        for i, linha in enumerate(cursor.fetchall()):
            # Renderiza linhas alternando cores discretamente (efeito zebra)
            tag = "par" if i % 2 == 0 else "impar"
            tabela.insert("", tk.END, values=linha, tags=(tag,))
        
        tabela.tag_configure("par", background=COR_CARD)
        tabela.tag_configure("impar", background="#f8fafc")
        conn.close()

    ent_busca.bind("<KeyRelease>", lambda e: carregar_dados(ent_busca.get()))

    # Lógica Editar
    def executar_edicao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma raça na tabela para editar!")
            return

        valores = tabela.item(item, "values")
        id_raca = valores[0]

        abrir_cadastro_raca(
            container,
            lambda: abrir_consulta_raca(container, voltar),
            id_raca=id_raca
        )

    # Lógica Excluir
    def executar_exclusao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma raça na tabela para excluir!")
            return

        valores = tabela.item(item, "values")
        id_raca = valores[0]
        nome = valores[1]

        confirmar = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a raça '{nome}'?")
        if confirmar:
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM raca WHERE id_raca = ?", (id_raca,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Raça excluída com sucesso!")
                carregar_dados()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Não é possível excluir esta raça pois existem pets cadastrados com ela.")

    # RODAPÉ (BOTÕES)
    frame_botoes = tk.Frame(conteudo, bg=COR_BG)
    frame_botoes.pack(fill="x", pady=(15, 0))

    btn_voltar = tk.Button(frame_botoes, text="VOLTAR", bg=COR_NEUTRO, fg=COR_TEXTO, width=12, command=voltar)
    btn_voltar.pack(side="left", ipady=6)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER)

    btn_excluir = tk.Button(frame_botoes, text="EXCLUIR", bg=COR_ALERTA, fg="white", width=12, command=executar_exclusao)
    btn_excluir.pack(side="right", ipady=6, padx=(10, 0))
    estilizar_botao(btn_excluir, COR_ALERTA, COR_ALERTA_HOVER)

    btn_editar = tk.Button(frame_botoes, text="EDITAR RAÇA", bg=COR_PRIMARIA, fg="white", width=14, command=executar_edicao)
    btn_editar.pack(side="right", ipady=6)
    estilizar_botao(btn_editar, COR_PRIMARIA, COR_PRIMARIA_HOVER)

    carregar_dados()

