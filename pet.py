import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
 
# =========================
# BANCO DE DADOS
# =========================
 
def conectar():
    conn = sqlite3.connect("db_projeto_integrador.db", timeout=30)
    cursor = conn.cursor()
 
    cursor.execute("PRAGMA foreign_keys = ON")
 
    # Criando a tabela de pets baseada na lógica do seu segundo código
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pet (
            id_pet INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_pet VARCHAR(100) NOT NULL,
            porte VARCHAR(50) NOT NULL,
            idade VARCHAR(50) NOT NULL,
            id_raca INTEGER NOT NULL,
            id_especie INTEGER NOT NULL,
            CONSTRAINT fk_pet_raca FOREIGN KEY (id_raca) REFERENCES categoria(id_raca),
            CONSTRAINT fk_pet_especie FOREIGN KEY (id_especie) REFERENCES categoria(id_especie)
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
    cursor.execute("""
        SELECT id_especie, nome_especie
        FROM categoria
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados
 
def obter_raca():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_raca, nome_raca
        FROM categoria
    """)
    dados = cursor.fetchall()
    conn.close()
    return dados
 
# =========================
# CADASTRO / EDIÇÃO
# =========================
 
def abrir_cadastro_pet(container, voltar, id_pet=None):
    limpar_tela(container)
   
    frame = tk.Frame(container)
    frame.pack(fill="both", expand=True)
 
    titulo = "EDITAR PET" if id_pet else "CADASTRAR PET"
 
    tk.Label(
        frame,
        text=titulo,
        font=("Arial", 14, "bold")
    ).pack(pady=20)
 
    # NOME
    tk.Label(frame, text="Nome do Pet:").pack()
    ent_nome = tk.Entry(frame, width=40)
    ent_nome.pack(pady=5)
 
    # PORTE (Corrigido o nome da variável)
    tk.Label(frame, text="Porte do Pet:").pack()
    ent_porte = tk.Entry(frame, width=40)
    ent_porte.pack(pady=5)
 
    # IDADE (Corrigido o nome da variável)
    tk.Label(frame, text="Idade do Pet:").pack()
    ent_idade = tk.Entry(frame, width=40)
    ent_idade.pack(pady=5)
 
    # RAÇA
    lista_raca = obter_raca()
    nomes_raca = [c[1] for c in lista_raca]
 
    tk.Label(frame, text="Raça:").pack()
    combo_raca = ttk.Combobox(
        frame,
        values=nomes_raca,
        width=37,
        state="readonly"
    )
    combo_raca.pack(pady=5)
 
    # ESPÉCIE
    lista_especie = obter_especies()
    nomes_especie = [e[1] for e in lista_especie]
 
    tk.Label(frame, text="Espécie:").pack()
    combo_especie = ttk.Combobox(
        frame,
        values=nomes_especie,
        width=37,
        state="readonly"
    )
    combo_especie.pack(pady=5)
 
    # =========================
    # CARREGAR DADOS EDIÇÃO
    # =========================
    if id_pet:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT nome_pet, porte, idade, id_raca, id_especie
            FROM pet
            WHERE id_pet = ?
        """, (id_pet,))
        resultado = cursor.fetchone()
        conn.close()
 
        if resultado:
            nome, porte, idade, id_rac, id_esp = resultado
 
            ent_nome.insert(0, nome)
            ent_porte.insert(0, porte)
            ent_idade.insert(0, idade)
 
            ids_rac = [r[0] for r in lista_raca]
            if id_rac in ids_rac:
                combo_raca.current(ids_rac.index(id_rac))
 
            ids_esp = [e[0] for e in lista_especie]
            if id_esp in ids_esp:
                combo_especie.current(ids_esp.index(id_esp))
 
    # =========================
    # LÓGICA DE SALVAR
    # =========================
    def salvar():
        nome = ent_nome.get().strip()
        porte = ent_porte.get().strip()
        idade = ent_idade.get().strip()
 
        if not nome or not porte or not idade:
            messagebox.showwarning("Aviso", "Todos os campos de texto devem ser preenchidos.")
            return
 
        idx_rac = combo_raca.current()
        idx_esp = combo_especie.current()
 
        if idx_rac == -1:
            messagebox.showwarning("Aviso", "Selecione uma raça.")
            return
 
        if idx_esp == -1:
            messagebox.showwarning("Aviso", "Selecione uma espécie.")
            return
 
        id_raca = lista_raca[idx_rac][0]
        id_especie = lista_especie[idx_esp][0]
 
        conn = conectar()
        cursor = conn.cursor()
 
        if id_pet:
            cursor.execute("""
                UPDATE pet
                SET nome_pet = ?, porte = ?, idade = ?, id_raca = ?, id_especie = ?
                WHERE id_pet = ?
            """, (nome, porte, idade, id_raca, id_especie, id_pet))
            mensagem = "Pet atualizado com sucesso!"
        else:
            cursor.execute("""
                INSERT INTO pet (nome_pet, porte, idade, id_raca, id_especie)
                VALUES (?, ?, ?, ?, ?)
            """, (nome, porte, idade, id_raca, id_especie))
            mensagem = "Pet cadastrado com sucesso!"
 
        conn.commit()
        conn.close()
 
        messagebox.showinfo("Sucesso", mensagem)
        voltar()
 
    # =========================
    # BOTÕES
    # =========================
    frame_botoes = tk.Frame(frame)
    frame_botoes.pack(pady=20)
 
    texto_botao = "ATUALIZAR" if id_pet else "SALVAR"
    cor_botao = "#ffcc00" if id_pet else "lightgreen"
 
    tk.Button(
        frame_botoes,
        text=texto_botao,
        bg=cor_botao,
        width=15,
        command=salvar
    ).pack(side="left", padx=5)
 
    tk.Button(
        frame_botoes,
        text="VOLTAR",
        width=15,
        bg="#cccccc",
        command=voltar
    ).pack(side="left", padx=5)
 
 
# =========================
# CONSULTA
# =========================
 
def abrir_consulta_pet(container, voltar):
    limpar_tela(container)
 
    frame = tk.Frame(container)
    frame.pack(fill="both", expand=True)
 
    tk.Label(
        frame,
        text="CONSULTA DE PETS",
        font=("Arial", 14, "bold")
    ).pack(pady=20)
 
    # BUSCA
    frame_busca = tk.Frame(frame)
    frame_busca.pack(pady=10)
 
    tk.Label(frame_busca, text="Buscar:").pack(side="left", padx=5)
    ent_busca = tk.Entry(frame_busca, width=25)
    ent_busca.pack(side="left", padx=5)
 
    # TABELA
    colunas = ("ID", "Nome", "Porte", "Idade", "Raça", "Espécie")
    tabela = ttk.Treeview(frame, columns=colunas, show="headings")
 
    for coluna in colunas:
        tabela.heading(coluna, text=coluna)
 
    tabela.column("ID", width=50, anchor="center")
    tabela.column("Nome", width=120)
    tabela.column("Porte", width=80, anchor="center")
    tabela.column("Idade", width=80, anchor="center")
    tabela.column("Raça", width=100)
    tabela.column("Espécie", width=100)
 
    tabela.pack(pady=20, padx=10, fill="both", expand=True)
 
    # CARREGAR DADOS
    def carregar_dados(filtro=""):
        for row in tabela.get_children():
            tabela.delete(row)
 
        conn = conectar()
        cursor = conn.cursor()
 
        # Query adaptada com LEFT JOIN para buscar os nomes na tabela categoria
        # Como seu db usa a tabela 'categoria' para ambos, referenciamos aliases diferentes (r e e)
        query_base = """
            SELECT p.id_pet, p.nome_pet, p.porte, p.idade, r.nome_raca, e.nome_especie
            FROM pet p
            LEFT JOIN categoria r ON p.id_raca = r.id_raca
            LEFT JOIN categoria e ON p.id_especie = e.id_especie
        """
 
        if filtro:
            cursor.execute(query_base + " WHERE LOWER(p.nome_pet) LIKE LOWER(?)", ('%' + filtro + '%',))
        else:
            cursor.execute(query_base)
 
        for linha in cursor.fetchall():
            tabela.insert("", tk.END, values=linha)
 
        conn.close()
 
    # BUSCA EM TEMPO REAL
    ent_busca.bind("<KeyRelease>", lambda e: carregar_dados(ent_busca.get()))
 
    # EDITAR
    def executar_edicao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um pet!")
            return
 
        valores = tabela.item(item, "values")
        id_pet = valores[0]
 
        abrir_cadastro_pet(
            container,
            lambda: abrir_consulta_pet(container, voltar),
            id_pet=id_pet
        )
 
    # EXCLUIR
    def executar_exclusao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um pet!")
            return
 
        valores = tabela.item(item, "values")
        id_pet = valores[0]
        nome = valores[1]
 
        confirmar = messagebox.askyesno("Confirmar exclusão", f"Excluir '{nome}'?")
        if confirmar:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pet WHERE id_pet = ?", (id_pet,))
            conn.commit()
            conn.close()
 
            messagebox.showinfo("Sucesso", "Pet excluído!")
            carregar_dados()
 
    # BOTÕES
    frame_botoes = tk.Frame(frame)
    frame_botoes.pack(pady=10)
 
    tk.Button(frame_botoes, text="EDITAR", bg="#ffcc00", width=15, command=executar_edicao).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="EXCLUIR", bg="#ff6b6b", fg="white", width=15, command=executar_exclusao).pack(side="left", padx=5)
    tk.Button(frame_botoes, text="VOLTAR", width=15, bg="#cccccc", command=voltar).pack(side="left", padx=5)
    
    carregar_dados()