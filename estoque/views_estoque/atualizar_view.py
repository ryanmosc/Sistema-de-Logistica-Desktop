import tkinter as tk
from tkinter import ttk
from estoque.functions.atualizar import enviar_att

def exibir_formulario_atualizacao(janela_pai, dados_produto):
    
    janela_atualizar = tk.Toplevel(janela_pai)
    janela_atualizar.title("Atualizar Produto")
    janela_atualizar.geometry("400x400")

    tk.Label(janela_atualizar, text="Atualizar Produto", font=("Arial", 14, "bold")).pack(pady=10)
    form_frame = tk.Frame(janela_atualizar)
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
        else:
            entrada = tk.Entry(form_frame)
            entrada.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = entrada

    # Preenche os dados nos campos
    if dados_produto:
        entradas["Nome do Produto"].insert(0, dados_produto[1])
        entradas["Estoque"].insert(0, dados_produto[2])
        entradas["Categoria"].set(dados_produto[3])
        entradas["Preço de Custo"].insert(0, str(dados_produto[4]))
        entradas["Preço de Venda"].insert(0, str(dados_produto[5]))

    tk.Button(
    janela_atualizar, 
    text="Atualizar", 
    command=lambda: enviar_att(entradas, dados_produto[0])
    ).pack(pady=15)

    tk.Button(janela_atualizar, text="Fechar", command=janela_atualizar.destroy).pack(pady=5)
