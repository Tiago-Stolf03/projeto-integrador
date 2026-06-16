import tkinter as tk

def ir_para_tela_2():
    # Remove a tela 1 da visualização
    frame_tela1.pack_forget()
    # Mostra a tela 2
    frame_tela2.pack(fill="both", expand=True)

janela = tk.Tk()
janela.geometry("300x200")

# --- ESTRUTURA DA TELA 1 ---
frame_tela1 = tk.Frame(janela, bg="lightgreen")
frame_tela1.pack(fill="both", expand=True)

label1 = tk.Label(frame_tela1, text="Esta é a Tela Inicial", bg="lightgreen")
label1.pack(pady=20)

botao1 = tk.Button(frame_tela1, text="Ir para Tela 2", command=ir_para_tela_2)
botao1.pack()

# --- ESTRUTURA DA TELA 2 (Fica oculta no início) ---
frame_tela2 = tk.Frame(janela, bg="lightblue")

label2 = tk.Label(frame_tela2, text="Esta é a Nova Tela!", bg="lightblue")
label2.pack(pady=20)

janela.mainloop()