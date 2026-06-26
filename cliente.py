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
    conn = sqlite3.connect(os.path.join(BASE_DIR, "db_projeto_integrador.db"), timeout=30)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente VARCHAR(50) NOT NULL,
            cpf VARCHAR(50) NOT NULL UNIQUE,
            endereco VARCHAR(50) NOT NULL,
            telefone VARCHAR(50) NOT NULL
        )
    """)
    conn.commit()
    return conn

def limpar_tela(container):
    for widget in container.winfo_children():
        widget.destroy()

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
def abrir_cadastro_cliente(container, voltar, id_cliente=None):
    limpar_tela(container)
    container.configure(bg=COR_BG)
    
    titulo = "Editar Cliente" if id_cliente else "Cadastrar Cliente"
    criar_header(container, titulo)

    card = tk.Frame(container, bg=COR_CARD, highlightthickness=1, highlightbackground="#e2e8f0")
    card.place(relx=0.5, rely=0.5, anchor="center", width=460, height=450)

    form_frame = tk.Frame(card, bg=COR_CARD)
    form_frame.pack(fill="both", expand=True, padx=35, pady=20)

    # Apenas letras
    def validar_apenas_letras(texto_inserido):
        return all(char.isalpha() or char.isspace() for char in texto_inserido)

    validador_nome = form_frame.register(validar_apenas_letras)

    # CAMPO NOME 
    tk.Label(form_frame, text="Nome do Cliente", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(anchor="w", pady=(5, 2))
    ent_nome = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#f1f5f9", fg=COR_TEXTO, relief="flat", validate="key", validatecommand=(validador_nome, "%P"))
    ent_nome.pack(fill="x", ipady=5, pady=(0, 10))

    # CAMPO CPF 
    tk.Label(form_frame, text="CPF (apenas números)", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(anchor="w", pady=(5, 2))
    ent_cpf = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#f1f5f9", fg=COR_TEXTO, relief="flat")
    ent_cpf.pack(fill="x", ipady=5, pady=(0, 10))

    # CAMPO ENDEREÇO 
    tk.Label(form_frame, text="Endereço Residencial", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(anchor="w", pady=(5, 2))
    ent_endereco = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#f1f5f9", fg=COR_TEXTO, relief="flat")
    ent_endereco.pack(fill="x", ipady=5, pady=(0, 10))

    # CAMPO TELEFONE 
    tk.Label(form_frame, text="Telefone com DDD", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(anchor="w", pady=(5, 2))
    ent_telefone = tk.Entry(form_frame, font=("Segoe UI", 10), bg="#f1f5f9", fg=COR_TEXTO, relief="flat")
    ent_telefone.pack(fill="x", ipady=5, pady=(0, 20))

    def formatar_cpf(event):
        text = ent_cpf.get()
        digits = "".join([c for c in text if c.isdigit()])[:11]
        formatted = ""
        if len(digits) <= 3:
            formatted = digits
        elif len(digits) <= 6:
            formatted = f"{digits[:3]}.{digits[3:]}"
        elif len(digits) <= 9:
            formatted = f"{digits[:3]}.{digits[3:6]}.{digits[6:]}"
        else:
            formatted = f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
        ent_cpf.delete(0, tk.END)
        ent_cpf.insert(0, formatted)

    def formatar_telefone(event):
        text = ent_telefone.get()
        digits = "".join([c for c in text if c.isdigit()])[:11]
        formatted = ""
        if len(digits) <= 2:
            formatted = digits
        elif len(digits) <= 6:
            formatted = f"({digits[:2]}) {digits[2:]}"
        elif len(digits) <= 10:
            formatted = f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
        else:
            formatted = f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
        ent_telefone.delete(0, tk.END)
        ent_telefone.insert(0, formatted)

    ent_cpf.bind("<KeyRelease>", formatar_cpf)
    ent_telefone.bind("<KeyRelease>", formatar_telefone)

    if id_cliente:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome_cliente, cpf, endereco, telefone FROM cliente WHERE id_cliente = ?", (id_cliente,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            nome, cpf, endereco, telefone = resultado
            ent_nome.insert(0, nome)
            ent_cpf.insert(0, cpf)
            ent_endereco.insert(0, endereco)
            ent_telefone.insert(0, telefone)

    # Salvar
    def salvar():
        nome = ent_nome.get().strip()
        cpf = ent_cpf.get().strip()
        endereco = ent_endereco.get().strip()
        telefone = ent_telefone.get().strip()

        if not nome or not cpf or not endereco or not telefone:
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos.")
            return

        if len(cpf) < 14:
            messagebox.showwarning("Aviso", "O CPF digitado está incompleto.")
            return
            
        if len(telefone) < 13:
            messagebox.showwarning("Aviso", "O Telefone digitado está incompleto.")
            return

        conn = conectar()
        cursor = conn.cursor()
        sucesso = False

        try:
            if id_cliente:
                cursor.execute("""
                    UPDATE cliente SET nome_cliente = ?, cpf = ?, endereco = ?, telefone = ? WHERE id_cliente = ?
                """, (nome, cpf, endereco, telefone, id_cliente))
                mensagem = "Cliente atualizado com sucesso!"
            else:
                cursor.execute("""
                    INSERT INTO cliente (nome_cliente, cpf, endereco, telefone) VALUES (?, ?, ?, ?)
                """, (nome, cpf, endereco, telefone))
                mensagem = "Cliente cadastrado com sucesso!"

            conn.commit()
            sucesso = True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este CPF já está cadastrado para outro cliente.")
        finally:
            conn.close()

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            voltar()

    # Botões do Card
    frame_botoes = tk.Frame(form_frame, bg=COR_CARD)
    frame_botoes.pack(fill="x", pady=(10, 0))

    btn_voltar = tk.Button(frame_botoes, text="VOLTAR", command=voltar, width=12)
    btn_voltar.pack(side="left", ipady=5)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER, cor_texto=COR_TEXTO)

    texto_botao = "ATUALIZAR" if id_cliente else "SALVAR"
    btn_salvar = tk.Button(frame_botoes, text=texto_botao, command=salvar, width=14)
    btn_salvar.pack(side="right", ipady=5)
    estilizar_botao(btn_salvar, COR_PRIMARIA, COR_PRIMARIA_HOVER)



# CONSULTA
def abrir_consulta_cliente(container, voltar):
    limpar_tela(container)
    container.configure(bg=COR_BG)

    criar_header(container, "Consulta de Clientes")

    conteudo = tk.Frame(container, bg=COR_BG)
    conteudo.pack(fill="both", expand=True, padx=25, pady=20)

    # BARRA DE BUSCA
    frame_busca = tk.Frame(conteudo, bg=COR_BG)
    frame_busca.pack(fill="x", pady=(0, 15))

    tk.Label(frame_busca, text="Buscar por Nome:", font=("Segoe UI", 10, "bold"), fg=COR_TEXTO, bg=COR_BG).pack(side="left", padx=(0, 10))
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

    colunas = ("ID", "Nome", "CPF", "Endereço", "Telefone")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", style="Treeview")

    for coluna in colunas:
        tabela.heading(coluna, text=coluna, anchor="w" if coluna != "ID" and coluna != "CPF" and coluna != "Telefone" else "center")

    tabela.column("ID", width=50, anchor="center")
    tabela.column("Nome", width=150, anchor="w")
    tabela.column("CPF", width=110, anchor="center")
    tabela.column("Endereço", width=180, anchor="w")
    tabela.column("Telefone", width=110, anchor="center")

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
    tabela.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def carregar_dados(filtro=""):
        for row in tabela.get_children():
            tabela.delete(row)

        conn = conectar()
        cursor = conn.cursor()
        query_base = "SELECT id_cliente, nome_cliente, cpf, endereco, telefone FROM cliente"

        if filtro:
            cursor.execute(query_base + " WHERE LOWER(nome_cliente) LIKE LOWER(?)", ('%' + filtro + '%',))
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
            messagebox.showwarning("Aviso", "Selecione um cliente para editar!")
            return

        id_cliente = tabela.item(item, "values")[0]
        abrir_cadastro_cliente(container, lambda: abrir_consulta_cliente(container, voltar), id_cliente=id_cliente)

    # Lógica de Exclusão
    def executar_exclusao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir!")
            return

        valores = tabela.item(item, "values")
        id_cliente, nome = valores[0], valores[1]

        if messagebox.askyesno("Confirmar Exclusão", f"Deseja realmente excluir o cliente '{nome}'?"):
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cliente WHERE id_cliente = ?", (id_cliente,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
            carregar_dados()

    # Rodapé 
    frame_botoes = tk.Frame(conteudo, bg=COR_BG)
    frame_botoes.pack(fill="x", pady=(15, 0))

    btn_voltar = tk.Button(frame_botoes, text="VOLTAR", command=voltar, width=12)
    btn_voltar.pack(side="left", ipady=5)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER, cor_texto=COR_TEXTO)

    btn_excluir = tk.Button(frame_botoes, text="EXCLUIR", command=executar_exclusao, bg=COR_ALERTA, width=12)
    btn_excluir.pack(side="right", ipady=5, padx=(10, 0))
    estilizar_botao(btn_excluir, COR_ALERTA, COR_ALERTA_HOVER)

    btn_editar = tk.Button(frame_botoes, text="EDITAR", command=executar_edicao, width=12)
    btn_editar.pack(side="right", ipady=5)
    estilizar_botao(btn_editar, COR_PRIMARIA, COR_PRIMARIA_HOVER)

    carregar_dados()