import tkinter as tk
from tkinter import ttk
from estoque.functions.cadastrar import enviar
from home.home import abrir_tela_estoque


def exibir_formulario_cadastro(janela_pai):
    janela_cadastro = tk.Toplevel(janela_pai)
    janela_cadastro.title("Cadastro de Produto")
    janela_cadastro.geometry("400x400")

    tk.Label(janela_cadastro, text="Cadastro de Produto", font=("Arial", 14, "bold")).pack(pady=10)
    form_frame = tk.Frame(janela_cadastro)
    form_frame.pack(pady=10)

    entradas = {}

    categorias_opcoes = ["ALIMENTO", "LIMPEZA", "HIGIENE", "BEBIDAS", "OUTROS"]
    


    campos = [
        "Nome do Produto",
        "Categoria",  
        "Estoque",
        "Preço de Custo",
        "Preço de Venda"
    ]

    for idx, campo in enumerate(campos):
        tk.Label(form_frame, text=campo).grid(row=idx, column=0, sticky="e", pady=5, padx=5)

        if campo == "Categoria":
            combobox = ttk.Combobox(form_frame, values=categorias_opcoes, state="readonly")
            combobox.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = combobox
            combobox.current(4) 
        else:
            entrada = tk.Entry(form_frame)
            entrada.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = entrada

    tk.Button(janela_cadastro, text="Salvar", command=lambda: enviar(entradas)).pack(pady=15)
    tk.Button(janela_cadastro, text="Fechar", command=janela_cadastro.destroy).pack(pady=5)
