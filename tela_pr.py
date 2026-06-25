import tkinter as tk
import raca
import especie
import raca
import especie
import adotar
import datetime
import backup


# CONFIGURAÇÃO DE CORES 

COR_BG = "#f8fafc"            # Fundo da tela 
COR_HEADER = "#0f172a"        # Fundo do Header 
COR_TEXTO_HEADER = "#ffffff"   # Texto do Header
COR_TEXTO = "#1e293b"         # Texto principal 

# Cores botões
COR_PRIMARIA = "#0ea5e9"      # Azul Moderno 
COR_PRIMARIA_HOVER = "#0284c7"
COR_NEUTRO = "#e2e8f0"        # Cinza claro para botões de voltar 
COR_NEUTRO_HOVER = "#cbd5e1"
COR_BACKUP = "#10b981"        # Verde para destaque do Backup 
COR_BACKUP_HOVER = "#059669"
COR_SAIR = "#d61a49" #vermelho sair
COR_SAIR_HOVER =  "#910528" #vermelho sair


# limpa a tela
def limpar_tela():
    for widget in container.winfo_children():
        widget.destroy()

def centralizar_janela(root, largura, altura):
    root.update_idletasks()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela // 2) - (largura // 2)
    y = (altura_tela // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{x}+{y}")

def criar_header(titulo):
    header = tk.Frame(container, bg=COR_HEADER, height=60)
    header.pack(fill="x", side="top")
    header.pack_propagate(False)
    
    lbl_titulo = tk.Label(header, text=titulo.upper(), font=("Segoe UI", 12, "bold"), fg=COR_TEXTO_HEADER, bg=COR_HEADER)
    lbl_titulo.pack(side="left", padx=20, pady=15)
    return header

def estilizar_botao(botao, cor_padrao, cor_hover, cor_texto="white"):
    botao.configure(bg=cor_padrao, fg=cor_texto, relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2", overrelief="flat")
    botao.bind("<Enter>", lambda e: botao.configure(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.configure(bg=cor_padrao))


# JANELA PRINCIPAL
root = tk.Tk()
root.title("Pet Match - Sistema de Adoção")
centralizar_janela(root, 1920, 1080) # Ajustado levemente para acomodar os headers de forma fluida
root.configure(bg=COR_BG)
root.state("zoomed")

container = tk.Frame(root, bg=COR_BG)
container.pack(fill="both", expand=True)


# MONTAGEM DAS TELAS
def tela_menu_consulta():
    limpar_tela()
    criar_header("Menu de Consultas")

    menu_frame = tk.Frame(container, bg=COR_BG)
    menu_frame.pack(fill="both", expand=True, padx=40, pady=20)

    botoes = [("Pet", lambda: raca.abrir_consulta_pet(container, tela_menu_consulta)),
        ("Espécie", lambda: especie.abrir_consulta_especie(container, tela_menu_consulta)),
        ("Raça", lambda: raca.abrir_consulta_raca(container, tela_menu_consulta)),
        ("Cliente", lambda: especie.abrir_consulta_cliente(container, tela_menu_consulta)),
        ("Visualizar Adoções", lambda: adotar.abrir_consulta_adocao(container, tela_menu_consulta))
    ]

    for texto, comando in botoes:
        btn = tk.Button(menu_frame, text=texto, command=comando)
        btn.pack(fill="x", pady=6, ipady=6)
        estilizar_botao(btn, COR_PRIMARIA, COR_PRIMARIA_HOVER)

    btn_voltar = tk.Button(menu_frame, text="VOLTAR", command=tela_principal)
    btn_voltar.pack(fill="x", pady=(20, 0), ipady=6)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER, cor_texto=COR_TEXTO)


def tela_menu_cadastro():
    limpar_tela()
    criar_header("Menu de Cadastros")

    menu_frame = tk.Frame(container, bg=COR_BG)
    menu_frame.pack(fill="both", expand=True, padx=40, pady=20)

    botoes = [
        ("Pet", lambda: raca.abrir_cadastro_pet(container, tela_menu_cadastro)),
        ("Espécie", lambda: especie.abrir_cadastro_especie(container, tela_menu_cadastro)),
        ("Raça", lambda: raca.abrir_cadastro_raca(container, tela_menu_cadastro)),
        ("Cliente", lambda: especie.abrir_cadastro_cliente(container, tela_menu_cadastro)),
        ("Registrar Adoções", lambda: adotar.abrir_cadastro_adocao(container, tela_menu_cadastro))
    ]

    for texto, comando in botoes:
        btn = tk.Button(menu_frame, text=texto, command=comando)
        btn.pack(fill="x", pady=6, ipady=6)
        estilizar_botao(btn, COR_PRIMARIA, COR_PRIMARIA_HOVER)

    btn_voltar = tk.Button(menu_frame, text="VOLTAR", command=tela_principal)
    btn_voltar.pack(fill="x", pady=(20, 0), ipady=6)
    estilizar_botao(btn_voltar, COR_NEUTRO, COR_NEUTRO_HOVER, cor_texto=COR_TEXTO)


def tela_principal():
    limpar_tela()
    criar_header("Pet Match")

    menu_frame = tk.Frame(container, bg=COR_BG)
    menu_frame.pack(fill="both", expand=True, padx=40, pady=40)

    # Botão Abrir Cadastro
    btn_cadastro = tk.Button(menu_frame, text="ABRIR CADASTROS", command=tela_menu_cadastro)
    btn_cadastro.pack(fill="x", pady=10, ipady=10)
    estilizar_botao(btn_cadastro, COR_PRIMARIA, COR_PRIMARIA_HOVER)

    # Botão Consultar Listas
    btn_consulta = tk.Button(menu_frame, text="CONSULTAR LISTAS", command=tela_menu_consulta)
    btn_consulta.pack(fill="x", pady=10, ipady=10)
    estilizar_botao(btn_consulta, COR_HEADER, "#1e293b")

    # Backup
    def acao_backup():
        data_atual = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_backup = f"./backup/backup_banco_{data_atual}.db"
        backup.realizar_backup('db_projeto_integrador.db', nome_backup)

    # botão backup
    btn_backup = tk.Button(menu_frame, text="REALIZAR BACKUP", command=acao_backup)
    btn_backup.pack(fill="x", pady=10, ipady=10)
    estilizar_botao(btn_backup, COR_BACKUP, COR_BACKUP_HOVER)

    btn_sair=tk.Button(menu_frame, text="SAIR", command=lambda:root.destroy(), width=260, height=2)
    btn_sair.place(relx=0.5, rely=0.9, anchor="center")
    estilizar_botao(btn_sair, COR_SAIR, COR_SAIR_HOVER)

tela_principal()

root.mainloop()