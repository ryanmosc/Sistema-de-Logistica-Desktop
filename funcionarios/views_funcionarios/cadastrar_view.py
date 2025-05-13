import tkinter as tk
from tkinter import ttk
from funcionarios.functions.cadastrar import enviar_funcionario  # Novo nome da função
from home.home import abrir_tela_funcionarios  # Voltar para tela de funcionários

def exibir_formulario_funcionario(janela_pai):
    janela_cadastro = tk.Toplevel(janela_pai)
    janela_cadastro.title("Cadastro de Funcionário")
    janela_cadastro.geometry("400x400")

    tk.Label(janela_cadastro, text="Cadastro de Funcionário", font=("Arial", 14, "bold")).pack(pady=10)
    form_frame = tk.Frame(janela_cadastro)
    form_frame.pack(pady=10)

    entradas = {}

    cargos_opcoes = [
        "Auxiliar de Estoque",
        "Supervisor de Logística",
        "Gerente Operacional",
        "Estagiário",
        "OUTROS"
    ]

    campos = [
        "Nome",
        "Sobrenome",
        "E-mail",
        "Telefone",
        "Cargo",
        "CPF",
        "Salário"
    ]

    for idx, campo in enumerate(campos):
        tk.Label(form_frame, text=campo).grid(row=idx, column=0, sticky="e", pady=5, padx=5)

        if campo == "Cargo":
            combobox = ttk.Combobox(form_frame, values=cargos_opcoes, state="readonly")
            combobox.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = combobox
            combobox.current(0)
        else:
            entrada = tk.Entry(form_frame)
            entrada.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = entrada

    tk.Button(janela_cadastro, text="Salvar", command=lambda: enviar_funcionario(entradas)).pack(pady=15)
    tk.Button(janela_cadastro, text="Fechar", command=janela_cadastro.destroy).pack(pady=5)
