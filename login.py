import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os

# CORES
COR_BG = "#f8fafc"            # Fundo da tela (Slate 50)
COR_CARD = "#ffffff"          # Fundo do bloco de login (Branco)
COR_TEXTO = "#1e293b"         # Texto principal (Slate 800)
COR_INPUT_BG = "#f1f5f9"      # Fundo dos campos de texto (Slate 100)

# Cores 
COR_PRIMARIA = "#0ea5e9"      # Azul Moderno (Sky 500)
COR_PRIMARIA_HOVER = "#0284c7"

def centralizar_janela(root, largura, altura):
    root.update_idletasks()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")

def estilizar_botao(botao, cor_padrao, cor_hover):
    botao.configure(bg=cor_padrao, fg="white", relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2", overrelief="flat")
    botao.bind("<Enter>", lambda e: botao.configure(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.configure(bg=cor_padrao))

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_banco = os.path.join(diretorio_atual, "db_projeto_integrador.db")

def verificar_login():
    email = entry_usuario.get().strip()
    senha = entry_senha.get()
    
    try:
        conn = sqlite3.connect(caminho_banco)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM usuario WHERE login = ? AND senha = ?", (email, senha))
        
        resultado = cursor.fetchone()
        conn.close()
        
        if resultado:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            janela.destroy() 
            subprocess.Popen(["python", "tela_pr.py"])
        else:
            messagebox.showerror("Erro", "Email ou senha incorretos.")
            
    except sqlite3.OperationalError as e:
        messagebox.showerror("Erro de Banco", f"Não foi possível acessar o banco:\n{e}")

# icones da sennha
def alternar_senha():
    if entry_senha.cget("show") == "*":
        entry_senha.configure(show="")
        btn_olho.configure(text="🔓")  # Símbolo simples de cadeado aberto ao mostrar
    else:
        entry_senha.configure(show="*")
        btn_olho.configure(text="👁")  # Olho simples quando oculto

# Configuração da Janela
janela = tk.Tk()
janela.title("Acesso ao Sistema")
centralizar_janela(janela, 360, 350)
janela.configure(bg=COR_BG)

# Card Central de Login
card = tk.Frame(janela, bg=COR_CARD, highlightthickness=1, highlightbackground="#e2e8f0")
card.pack(fill="both", expand=True, padx=25, pady=25)

# Título 
tk.Label(card, text="PET MATCH LOGIN", font=("Segoe UI", 14, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(pady=(20, 15))

#  CAMPO USUÁRIO 
frame_user_label = tk.Frame(card, bg=COR_CARD)
frame_user_label.pack(fill="x", padx=25, pady=(5, 2))

tk.Label(frame_user_label, text="👤 Email do Usuário", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(side="left")

entry_usuario = tk.Entry(card, font=("Segoe UI", 11), bg=COR_INPUT_BG, fg=COR_TEXTO, relief="flat", insertbackground=COR_TEXTO)
entry_usuario.pack(fill="x", padx=25, ipady=5, pady=(0, 10))

# CAMPO SENHA 
frame_senha_label = tk.Frame(card, bg=COR_CARD)
frame_senha_label.pack(fill="x", padx=25, pady=(5, 2))

tk.Label(frame_senha_label, text="🔒 Senha", font=("Segoe UI", 9, "bold"), fg=COR_TEXTO, bg=COR_CARD).pack(side="left")

# Container do input de senha
container_senha = tk.Frame(card, bg=COR_INPUT_BG)
container_senha.pack(fill="x", padx=25, pady=(0, 25))

# campo senha
entry_senha = tk.Entry(container_senha, show="*", font=("Segoe UI", 11), bg=COR_INPUT_BG, fg=COR_TEXTO, relief="flat", insertbackground=COR_TEXTO)
entry_senha.pack(side="left", fill="x", expand=True, ipady=5, padx=(5, 0))

# Botão da senha
btn_olho = tk.Button(
    container_senha, text="👁", bg=COR_INPUT_BG, fg=COR_TEXTO, 
    relief="flat", activebackground=COR_INPUT_BG, font=("Segoe UI", 11),
    cursor="hand2", command=alternar_senha
)
btn_olho.pack(side="right", padx=8)

#  BOTÃO ENTRAR 
btn_login = tk.Button(card, text="ENTRAR NO SISTEMA", command=verificar_login)
btn_login.pack(fill="x", padx=25, ipady=6)
estilizar_botao(btn_login, COR_PRIMARIA, COR_PRIMARIA_HOVER)

janela.mainloop()