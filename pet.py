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
        CREATE TABLE IF NOT EXISTS pet (
            id_pet INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_pet VARCHAR(100) NOT NULL,
            porte VARCHAR(50) NOT NULL,
            idade VARCHAR(50) NOT NULL,
            id_raca INTEGER NOT NULL,
            id_especie INTEGER NOT NULL,
            status VARCHAR(20) DEFAULT 'Disponível',
            CONSTRAINT fk_pet_raca FOREIGN KEY (id_raca) REFERENCES raca(id_raca),
            CONSTRAINT fk_pet_especie FOREIGN KEY (id_especie) REFERENCES especie(id_especie)
        )
    """)

    try:
        cursor.execute("ALTER TABLE pet ADD COLUMN status VARCHAR(20) DEFAULT 'Disponível'")
    except sqlite3.OperationalError:
        pass

    conn.commit()
    return conn

def limpar_tela(container):
    for widget in container.winfo_children():
        widget.destroy()

def obter_especies():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_especie, nome_especie FROM especie")
    dados = cursor.fetchall()
    conn.close()
    return dados

def obter_raca(id_especie=None):
    conn = conectar()
    cursor = conn.cursor()
    if id_especie:
        cursor.execute("SELECT id_raca, nome_raca FROM raca WHERE id_especie = ?", (id_especie,))
    else:
        cursor.execute("SELECT id_raca, nome_raca FROM raca")
    dados = cursor.fetchall()
    conn.close()
    return dados


def criar_header(container, titulo):
    header = tk.Frame(container, bg=COR_HEADER, height=60)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
    
    lbl_titulo = tk.Label(header, text=titulo.upper(), font=("Segoe UI", 14, "bold"), fg=COR_TEXTO_HEADER, bg=COR_HEADER)
    lbl_titulo.pack(side="left", padx=20, pady=15)
    return header

def estilizar_botao(botao, cor_padrao, cor_hover, cor_texto="white"):
    botao.configure(bg=cor_padrao, fg=cor_texto, relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2", overrelief="flat")
    botao.bind("<Enter>", lambda e: botao.configure(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.configure(bg=cor_padrao))


# CADASTRO / EDIÇÃO - tabela pet
def abrir_cadastro_pet(container, voltar, id_pet=None):
    limpar_tela(container)
    container.configure(bg=COR_BG)
    
    titulo = "Editar Pet" if id_pet else "Cadastrar Pet"
    criar_header(container, titulo)

    card = tk.Frame(container, bg=COR_CARD, highlightthickness=1, highlightbackground="#e2e8f0")
    card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=430)

    form_frame = tk.Frame(card, bg=COR_CARD)
    form_frame.pack(fill="both", expand=True, padx=35, pady=20)

    # Validar letras e numeros
    def validar_apenas_letras(texto_inserido):
        return all(char.isalpha() or char.isspace() for char in texto_inserido)

    def validar_apenas_numeros(texto_inserido):
        if texto_inserido == "": 
            return True
        if texto_inserido.isdigit():
            if int(texto_inserido) <= 200:
                return True
        return False

    validador_letras = form_frame.register(validar_apenas_letras)
    validador_idade = form_frame.register(validar_apenas_numeros)

    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=1)

    # Nome do Pet
    tk.Label(form_frame, text="Nome do Pet", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 2))
    ent_nome = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#f1f5f9", fg=COR_TEXTO, relief="flat", validate="key", validatecommand=(validador_letras, "%P"))
    ent_nome.grid(row=1, column=0, columnspan=2, sticky="ew", ipady=5, pady=(0, 12))

    # Porte do Pet
    opcoes_porte = ["Micro", "Pequeno", "Médio", "Grande"]
    tk.Label(form_frame, text="Porte", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).grid(row=2, column=0, sticky="w", pady=(0, 2))
    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Pet.TCombobox", fieldbackground="#f1f5f9", background="#e2e8f0", arrowcolor=COR_TEXTO, borderwidth=0)
    
    combo_porte = ttk.Combobox(form_frame, values=opcoes_porte, font=("Segoe UI", 9), state="readonly", style="Pet.TCombobox")
    combo_porte.grid(row=3, column=0, sticky="ew", padx=(0, 10), ipady=4, pady=(0, 12))

    # Idade do Pet
    tk.Label(form_frame, text="Idade (Anos)", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).grid(row=2, column=1, sticky="w", pady=(0, 2))
    ent_idade = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#f1f5f9", fg=COR_TEXTO, relief="flat", validate="key", validatecommand=(validador_idade, "%P"))
    ent_idade.grid(row=3, column=1, sticky="ew", ipady=5, pady=(0, 12))

    # Espécie
    lista_especie = obter_especies()
    nomes_especie = [e[1] for e in lista_especie]

    tk.Label(form_frame, text="Espécie", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).grid(row=4, column=0, sticky="w", pady=(0, 2))
    combo_especie = ttk.Combobox(form_frame, values=nomes_especie, font=("Segoe UI", 9), state="readonly", style="Pet.TCombobox")
    combo_especie.grid(row=5, column=0, sticky="ew", padx=(0, 10), ipady=4, pady=(0, 15))

    # Raça
    lista_raca = [] 
    tk.Label(form_frame, text="Raça", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).grid(row=4, column=1, sticky="w", pady=(0, 2))
    combo_raca = ttk.Combobox(form_frame, values=[], font=("Segoe UI", 9), state="disabled", style="Pet.TCombobox")
    combo_raca.grid(row=5, column=1, sticky="ew", ipady=4, pady=(0, 15))

    # pegar apenas a raça de acordo com a especie
    def atualizar_racas(event=None, selecionar_id_raca=None):
        nonlocal lista_raca
        idx_esp = combo_especie.current()
        
        if idx_esp != -1:
            id_especie = lista_especie[idx_esp][0]
            lista_raca = obter_raca(id_especie)
            nomes_raca = [r[1] for r in lista_raca]
            
            combo_raca.config(state="readonly", values=nomes_raca)
            combo_raca.set("")
            
            if selecionar_id_raca:
                ids_rac = [r[0] for r in lista_raca]
                if selecionar_id_raca in ids_rac:
                    combo_raca.current(ids_rac.index(selecionar_id_raca))
        else:
            combo_raca.config(state="disabled", values=[])
            combo_raca.set("")

    combo_especie.bind("<<ComboboxSelected>>", atualizar_racas)

    status_atual_edicao = "Disponível"
    if id_pet:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome_pet, porte, idade, id_raca, id_especie, status FROM pet WHERE id_pet = ?", (id_pet,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            nome, porte, idade, id_rac, id_esp, status_atual_edicao = resultado
            ent_nome.insert(0, nome)
            ent_idade.insert(0, idade)
            if porte in opcoes_porte:
                combo_porte.set(porte)

            ids_esp = [e[0] for e in lista_especie]
            if id_esp in ids_esp:
                combo_especie.current(ids_esp.index(id_esp))
                atualizar_racas(selecionar_id_raca=id_rac)

    # Salvar Dados
    def salvar():
        nome = ent_nome.get().strip()
        porte = combo_porte.get()
        idade = ent_idade.get().strip()

        if not nome or not idade:
            messagebox.showwarning("Aviso", "Os campos Nome e Idade devem ser preenchidos.")
            return
        if not porte:
            messagebox.showwarning("Aviso", "Selecione o porte do pet.")
            return

        idx_esp = combo_especie.current()
        idx_rac = combo_raca.current()

        if idx_esp == -1 or idx_rac == -1:
            messagebox.showwarning("Aviso", "Selecione a Espécie e a Raça.")
            return

        id_especie = lista_especie[idx_esp][0]
        id_raca = lista_raca[idx_rac][0]

        conn = conectar()
        cursor = conn.cursor()

        if id_pet:
            cursor.execute("""
                UPDATE pet SET nome_pet = ?, porte = ?, idade = ?, id_raca = ?, id_especie = ?, status = ?
                WHERE id_pet = ?
            """, (nome, porte, idade, id_raca, id_especie, status_atual_edicao, id_pet))
            mensagem = "Pet atualizado com sucesso!"
        else:
            cursor.execute("""
                INSERT INTO pet (nome_pet, porte, idade, id_raca, id_especie, status)
                VALUES (?, ?, ?, ?, ?, 'Disponível')
            """, (nome, porte, idade, id_raca, id_especie))
            mensagem = "Pet cadastrado com sucesso!"

        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", mensagem)
        voltar()

    # Rodapé do Card (Botões)
    frame_botoes = tk.Frame(form_frame, bg=COR_CARD)
    frame_botoes.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(15, 0))

    btn_voltar = tk.Button(frame_botoes, text="VOLTAR", command=voltar, width=12)
    btn_voltar.pack(side="left", ipady=6)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER, cor_texto=COR_TEXTO)

    texto_botao = "ATUALIZAR" if id_pet else "SALVAR PET"
    btn_salvar = tk.Button(frame_botoes, text=texto_botao, command=salvar, width=16)
    btn_salvar.pack(side="right", ipady=6)
    estilizar_botao(btn_salvar, COR_PRIMARIA, COR_PRIMARIA_HOVER)


# CONSULTA
def abrir_consulta_pet(container, voltar):
    limpar_tela(container)
    container.configure(bg=COR_BG)

    criar_header(container, "Consulta de Pets")

    conteudo = tk.Frame(container, bg=COR_BG)
    conteudo.pack(fill="both", expand=True, padx=25, pady=20)

    # BARRA DE BUSCA
    frame_busca = tk.Frame(conteudo, bg=COR_BG)
    frame_busca.pack(fill="x", pady=(0, 15))

    tk.Label(frame_busca, text="Buscar Pet:", font=("Segoe UI", 10, "bold"), fg=COR_TEXTO, bg=COR_BG).pack(side="left", padx=(0, 10))
    ent_busca = tk.Entry(frame_busca, font=("Segoe UI", 11), bg=COR_CARD, fg=COR_TEXTO, relief="solid", bd=1)
    ent_busca.configure(highlightbackground="#cbd5e1", highlightcolor=COR_PRIMARIA, highlightthickness=0)
    ent_busca.pack(side="left", fill="x", expand=True, ipady=4)

    # tabela consulta pet
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

    colunas = ("ID", "Nome", "Porte", "Idade", "Raça", "Espécie", "Status")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", style="Treeview")

    for coluna in colunas:
        align = "center" if coluna in ["ID", "Porte", "Idade", "Status"] else "w"
        tabela.heading(coluna, text=coluna, anchor=align)
        tabela.column(coluna, anchor=align)

    tabela.column("ID", width=45)
    tabela.column("Nome", width=130)
    tabela.column("Porte", width=80)
    tabela.column("Idade", width=65)
    tabela.column("Raça", width=110)
    tabela.column("Espécie", width=100)
    tabela.column("Status", width=100)

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    tabela.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def carregar_dados(filtro=""):
        for row in tabela.get_children():
            tabela.delete(row)

        conn = conectar()
        cursor = conn.cursor()

        query_base = """
        SELECT p.id_pet, p.nome_pet, p.porte, p.idade, r.nome_raca, e.nome_especie, 
               COALESCE(p.status, 'Disponível') as status
        FROM pet p
        LEFT JOIN raca r ON p.id_raca = r.id_raca
        LEFT JOIN especie e ON p.id_especie = e.id_especie
        """

        if filtro:
            cursor.execute(query_base + " WHERE LOWER(p.nome_pet) LIKE LOWER(?)", ('%' + filtro + '%',))
        else:
            cursor.execute(query_base)

        for i, linha in enumerate(cursor.fetchall()):
            tag = "par" if i % 2 == 0 else "impar"
            tabela.insert("", tk.END, values=linha, tags=(tag,))
        
        tabela.tag_configure("par", background=COR_CARD)
        tabela.tag_configure("impar", background="#f8fafc")
        conn.close()

    ent_busca.bind("<KeyRelease>", lambda e: carregar_dados(ent_busca.get()))

    def executar_edicao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um pet na lista para editar!")
            return
        id_pet = tabela.item(item, "values")[0]
        abrir_cadastro_pet(container, lambda: abrir_consulta_pet(container, voltar), id_pet=id_pet)

    def executar_exclusao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um pet na lista para excluir!")
            return
        valores = tabela.item(item, "values")
        id_pet, nome = valores[0], valores[1]

        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente remover o pet '{nome}'?"):
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pet WHERE id_pet = ?", (id_pet,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Pet removido com sucesso!")
            carregar_dados()

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