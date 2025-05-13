import tkinter as tk
from tkinter import ttk



def exibir_formulario_fornecedor(janela_pai):
    from fornecedores.functions.enviar_cadastro import enviar_fornecedores
    janela_fornecedor = tk.Toplevel(janela_pai)
    janela_fornecedor.title("Cadastro de Fornecedor")
    janela_fornecedor.geometry("400x450")

    tk.Label(janela_fornecedor, text="Cadastro de Fornecedor", font=("Arial", 14, "bold")).pack(pady=10)
    form_frame = tk.Frame(janela_fornecedor)
    form_frame.pack(pady=10)

    entradas = {}

    campos = [
        "Nome",
        "CNPJ",
        "Telefone",
        "Email",
        "Endereço"
    ]

    for idx, campo in enumerate(campos):
        tk.Label(form_frame, text=campo).grid(row=idx, column=0, sticky="e", pady=5, padx=5)
        entrada = tk.Entry(form_frame)
        entrada.grid(row=idx, column=1, pady=5, padx=5)
        entradas[campo] = entrada

    tk.Button(janela_fornecedor, text="Salvar", command=lambda: enviar_fornecedores(entradas)).pack(pady=15)
    tk.Button(janela_fornecedor, text="Fechar", command=janela_fornecedor.destroy).pack(pady=5)
