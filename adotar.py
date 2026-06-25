import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime
 
# =========================
# CONFIGURAÇÃO DE CORES (PALETA MODERNA)
# =========================
COR_BG = "#f8fafc"           # Fundo da tela (Slate 50)
COR_CARD = "#ffffff"         # Fundo de containers (Branco)
COR_HEADER = "#0f172a"       # Fundo do Header (Slate 900)
COR_TEXTO_HEADER = "#ffffff" # Texto do Header
COR_TEXTO = "#1e293b"        # Texto principal (Slate 800)
COR_MUTED = "#64748b"        # Texto secundário (Slate 500)
 
# Cores de Ação
COR_PRIMARIA = "#0ea5e9"     # Azul Moderno (Sky 500)
COR_PRIMARIA_HOVER = "#0284c7"
COR_ALERTA = "#e11d48"       # Vermelho/Rosa (Rose 600)
COR_ALERTA_HOVER = "#be123c"
COR_NEUTRO = "#e2e8f0"       # Cinza claro para botões secundários (Slate 200)
COR_NEUTRO_HOVER = "#cbd5e1"
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
# =========================
# BANCO DE DADOS
# =========================
 
def conectar():
    conn = sqlite3.connect(os.path.join(BASE_DIR, "db_projeto_integrador.db"), timeout=30)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
 
    # Criando a tabela de adocao
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adocao (
            id_ado INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_ado TEXT,
            id_pet INTEGER,
            id_cliente INTEGER,
            dat_ado TEXT,
            CONSTRAINT fk_id_cliente FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente),
            CONSTRAINT fk_id_pet FOREIGN KEY(id_pet) REFERENCES pet(id_pet)
        )
    """)
   
    # Alerta/Garantia: Adiciona a coluna de status na tabela pet caso ela não exista
    try:
        cursor.execute("ALTER TABLE pet ADD COLUMN status VARCHAR(20) DEFAULT 'Disponível'")
    except sqlite3.OperationalError:
        pass # A coluna já existe, tudo certo!
 
    conn.commit()
    return conn
 
def limpar_tela(container):
    for widget in container.winfo_children():
        widget.destroy()
 
def obter_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nome_cliente FROM cliente")
    dados = cursor.fetchall()
    conn.close()
    return dados
 
def obter_pets_disponiveis():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id_pet, nome_pet FROM pet WHERE status = 'Disponível' OR status IS NULL")
    dados = cursor.fetchall()
    conn.close()
    return dados
 
 
# =========================
# COMPONENTES VISUAIS CUSTOMIZADOS
# =========================
 
def criar_header(container, titulo):
    """Cria um cabeçalho moderno e destacado para a tela"""
    header = tk.Frame(container, bg=COR_HEADER, height=60)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
   
    lbl_titulo = tk.Label(header, text=titulo.upper(), font=("Segoe UI", 14, "bold"),fg=COR_TEXTO_HEADER, bg=COR_HEADER)
    lbl_titulo.pack(side="left", padx=20, pady=15)
    return header
 
def estilizar_botao(botao, cor_padrao, cor_hover):
    """Aplica o efeito hover e estilo flat aos botões"""
    botao.configure(relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2", overrelief="flat")
    botao.bind("<Enter>", lambda e: botao.configure(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.configure(bg=cor_padrao))
 
 
# TELA DE REGISTRAR ADOÇÃO
def abrir_cadastro_adocao(container, voltar):
    limpar_tela(container)
    container.configure(bg=COR_BG)
   
    criar_header(container, "Registrar Nova Adoção")
 
    card = tk.Frame(container, bg=COR_CARD, highlightthickness=0)
    card.configure(highlightbackground="#e2e8f0", highlightcolor="#e2e8f0", bd=0)
    card.place(relx=0.5, rely=0.5, anchor="center", width=480, height=360)
 
   
    form_frame = tk.Frame(card, bg=COR_CARD)
    form_frame.pack(fill="both", expand=True, padx=30, pady=25)
 
    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", fieldbackground="#f1f5f9", background="#e2e8f0", arrowcolor=COR_TEXTO, borderwidth=0)
 
    # SELEÇÃO DO CLIENTE
    lista_clientes = obter_clientes()
    nomes_clientes = [c[1] for c in lista_clientes]
 
    tk.Label(form_frame, text="Selecione o Cliente", font=("Segoe UI", 10, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(anchor="w", pady=(0, 5))
    combo_cliente = ttk.Combobox(form_frame, values=nomes_clientes, font=("Segoe UI", 10), state="readonly", style="TCombobox")
    combo_cliente.pack(fill="x", ipady=4, pady=(0, 15))
 
    # SELEÇÃO DO PET
    lista_pets = obter_pets_disponiveis()
    nomes_pets = [p[1] for p in lista_pets]
 
    tk.Label(form_frame, text="Selecione o Pet Disponível", font=("Segoe UI", 10, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(anchor="w", pady=(0, 5))
    combo_pet = ttk.Combobox(form_frame, values=nomes_pets, font=("Segoe UI", 10), state="readonly", style="TCombobox")
    combo_pet.pack(fill="x", ipady=4, pady=(0, 25))
 
    # SALVAR 
    def salvar():
        idx_cli = combo_cliente.current()
        idx_pet = combo_pet.current()
 
        if idx_cli == -1 or idx_pet == -1:
            messagebox.showwarning("Aviso", "Selecione um cliente e um pet para prosseguir.")
            return
 
        id_cliente = lista_clientes[idx_cli][0]
        id_pet = lista_pets[idx_pet][0]
       
        nome_ado = f"EMP_{id_cliente}_{id_pet}"
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
 
        conn = conectar()
        cursor = conn.cursor()
 
        try:
            cursor.execute("""
                INSERT INTO adocao (nome_ado, id_pet, id_cliente, dat_ado)
                VALUES (?, ?, ?, ?)
            """, (nome_ado, id_pet, id_cliente, data_atual))
 
            cursor.execute("UPDATE pet SET status = 'Indisponível' WHERE id_pet = ?", (id_pet,))
           
            conn.commit()
            messagebox.showinfo("Sucesso", f"Adoção registrada com o código: {nome_ado}")
            voltar()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Erro", f"Erro ao registrar adoção: {e}")
        finally:
            conn.close()
 
    # BOTÕES DO FORMULÁRIO
    frame_botoes = tk.Frame(form_frame, bg=COR_CARD)
    frame_botoes.pack(fill="x", side="bottom")
 
    btn_voltar = tk.Button(frame_botoes, text="VOLTAR", bg=COR_NEUTRO, fg=COR_TEXTO, width=12, command=voltar)
    btn_voltar.pack(side="left", ipady=6)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER)
 
    btn_salvar = tk.Button(frame_botoes, text="EFETIVAR ADOÇÃO", bg=COR_PRIMARIA, fg="white", width=18, command=salvar)
    btn_salvar.pack(side="right", ipady=6)
    estilizar_botao(btn_salvar, COR_PRIMARIA, COR_PRIMARIA_HOVER)
 
 
# CONSULTA DE ADOÇÕES

def abrir_consulta_adocao(container, voltar):
    limpar_tela(container)
    container.configure(bg=COR_BG)
 
    criar_header(container, "Histórico de Adoções Realizadas")
 
    conteudo = tk.Frame(container, bg=COR_BG)
    conteudo.pack(fill="both", expand=True, padx=30, pady=20)
 
    # (TREEVIEW)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background=COR_CARD, fieldbackground=COR_CARD,
                    foreground=COR_TEXTO, rowheight=30, font=("Segoe UI", 10), borderwidth=0)
    style.configure("Treeview.Heading",
                    background="#e2e8f0", foreground=COR_TEXTO,
                    font=("Segoe UI", 10, "bold"), relief="flat")
    style.map("Treeview", background=[("selected", "#e0f2fe")], foreground=[("selected", "#0369a1")])
 
    # container 
    frame_tabela = tk.Frame(conteudo, bg=COR_BG)
    frame_tabela.pack(fill="both", expand=True)
 
    colunas = ("ID Adoção", "Código Emp", "Nome Cliente", "Nome Pet", "Data Adoção", "ID Pet")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", style="Treeview")
 
    for coluna in colunas:
        tabela.heading(coluna, text=coluna, anchor="w" if "Nome" in coluna else "center")
 
    tabela.column("ID Adoção", width=80, anchor="center")
    tabela.column("Código Emp", width=120, anchor="center")
    tabela.column("Nome Cliente", width=160, anchor="w")
    tabela.column("Nome Pet", width=130, anchor="w")
    tabela.column("Data Adoção", width=140, anchor="center")
   
    
    tabela.column("ID Pet", width=0, minwidth=0, stretch=tk.NO)
 
    
    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)
    tabela.configure(yscrollcommand=scrollbar.set)
   
    tabela.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
 
    
    def carregar_dados():
        for row in tabela.get_children():
            tabela.delete(row)
 
        conn = conectar()
        cursor = conn.cursor()
 
        
        cursor.execute("""
            SELECT a.id_ado, a.nome_ado, c.nome_cliente, p.nome_pet, a.dat_ado, a.id_pet
            FROM adocao a
            INNER JOIN cliente c ON a.id_cliente = c.id_cliente
            INNER JOIN pet p ON a.id_pet = p.id_pet
        """)
 
        for i, linha in enumerate(cursor.fetchall()):
            tag = "par" if i % 2 == 0 else "impar"
            tabela.insert("", tk.END, values=linha, tags=(tag,))
       
        tabela.tag_configure("par", background=COR_CARD)
        tabela.tag_configure("impar", background="#f8fafc")
        conn.close()
 
    
    def executar_devolucao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione uma adoção na lista para processar a devolução.")
            return
 
        valores = tabela.item(item, "values")
        id_ado = valores[0]
        codigo_emp = valores[1]
        nome_pet = valores[3]
        id_pet = valores[5]
 
        confirmar = messagebox.askyesno(
            "Confirmar Devolução",
            f"Você confirma o retorno do pet '{nome_pet}' para a central?\nIsso removerá a adoção {codigo_emp}."
        )
       
        if confirmar:
            conn = conectar()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM adocao WHERE id_ado = ?", (id_ado,))
               
                cursor.execute("UPDATE pet SET status = 'Disponível' WHERE id_pet = ?", (id_pet,))
               
                conn.commit()
                messagebox.showinfo("Sucesso", f"O pet '{nome_pet}' voltou para a central e está Disponível para nova adoção!")
                carregar_dados()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Erro", f"Erro ao processar devolução: {e}")
            finally:
                conn.close()
 
    # RODAPÉ 
    frame_botoes = tk.Frame(conteudo, bg=COR_BG)
    frame_botoes.pack(fill="x", pady=(15, 0))
 
    btn_voltar = tk.Button(frame_botoes, text="VOLTAR", bg=COR_NEUTRO, fg=COR_TEXTO, width=12, command=voltar)
    btn_voltar.pack(side="left", ipady=6)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER)
 
    btn_devolver = tk.Button(frame_botoes, text="DEVOLVER PET", bg=COR_ALERTA, fg="white", width=16, command=executar_devolucao)
    btn_devolver.pack(side="right", ipady=6)
    estilizar_botao(btn_devolver, COR_ALERTA, COR_ALERTA_HOVER)
 
    carregar_dados()