import tkinter as tk
from tkinter import messagebox
from views.registro_view import tela_registro
from views.recuperar_senha_view import tela_recuperar_senha

def adicionar_usuario():
    messagebox.showinfo("Adicionar Usuário", "Função de adicionar usuário ainda não implementada.")

def alterar_senha():
    messagebox.showinfo("Alterar Senha", "Função de alterar senha ainda não implementada.")

def abrir_sobre(janela_atual=None):
    if janela_atual:
        janela_atual.destroy()  # Fecha a janela anterior

    sobre_janela = tk.Tk()  # Nova janela principal
    sobre_janela.title("Sobre o Sistema")
    sobre_janela.geometry("400x500")
    sobre_janela.resizable(False, False)

    # Nome do sistema
    tk.Label(sobre_janela, text="Sistema de Gerenciamento 2", font=("Arial", 14, "bold")).pack(pady=10)

    # Descrição
    descricao = (
        "Este sistema foi desenvolvido para gerenciar entradas, saídas, "
        "e informações de funcionários e usuários de forma prática e eficiente."
    )
    tk.Label(sobre_janela, text=descricao, wraplength=380, justify="center").pack(pady=10)

    # Tecnologias
    tk.Label(sobre_janela, text="Tecnologias utilizadas:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    tk.Label(sobre_janela, text="Python · Tkinter · PostgreSQL").pack()

    # Contato
    tk.Label(sobre_janela, text="Desenvolvido por Ryan Oliveira Moscardini", font=("Arial", 10, "bold")).pack(pady=(15, 5))
    contatos = (
        "LinkedIn: www.linkedin.com/in/ryan-moscardini-b7b6372ba\n"
        "GitHub: https://github.com/ryanmosc\n"
        "Telefone: +55 16 98175-9831\n"
        "E-mail: ryanoliveiramosc.com.098@gmail.com"
    )
    tk.Label(sobre_janela, text=contatos, justify="left", wraplength=380).pack()

    # Botões
    tk.Button(sobre_janela, text="Adicionar Usuário", width=25, command=lambda: tela_registro(sobre_janela)).pack(pady=5)
    tk.Button(sobre_janela, text="Trocar Senha", width=25, command=lambda: tela_recuperar_senha(sobre_janela)).pack(pady=5)
    # Botão de voltar para a home
    def voltar_para_home():
        from views.home_view import criar_tela_inicial
        sobre_janela.destroy()
        criar_tela_inicial()

    tk.Button(sobre_janela, text="Voltar", width=25, command=voltar_para_home).pack(pady=10)

    sobre_janela.mainloop()
