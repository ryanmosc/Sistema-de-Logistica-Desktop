from saidas.functions.saidas import enviar_saidas
import tkinter as tk
from tkinter import ttk
from saidas.functions.deletar_saisda import excluir_item_tabela
from saidas.functions.valor_saida import editar_quantidade_motivo
from saidas.functions.enviar_saidas import confirmar_todas_saidas

def exibir_formulario_saidas(janela_pai):
    janela_atualizar = tk.Toplevel(janela_pai)
    janela_atualizar.title("Saídas")
    janela_atualizar.geometry("1200x500")

    tk.Label(janela_atualizar, text="Saídas", font=("Arial", 14, "bold")).pack(pady=10)

    # Frame dos campos de entrada
    form_frame = tk.Frame(janela_atualizar)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Código de Barras:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entrada_codigo_barras = tk.Entry(form_frame, width=30)
    entrada_codigo_barras.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="ID do Produto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_id_produto = tk.Entry(form_frame, width=30)
    entrada_id_produto.grid(row=1, column=1, padx=5, pady=5)

    # Tabela (Treeview)
    tabela = ttk.Treeview(
        janela_atualizar,
        columns=("id", "nome", "categoria", "estoque", "quantidade", "motivo"),
        show="headings",
        height=10
    )
    for col in ("id", "nome", "categoria", "estoque", "quantidade", "motivo"):
        tabela.heading(col, text=col.capitalize())
        tabela.column(col, anchor="center")
    tabela.pack(fill="both", expand=True, padx=20, pady=10)

    # Frame de botões
    botoes_frame = tk.Frame(janela_atualizar)
    botoes_frame.pack(pady=5)

    # Primeira linha de botões
    tk.Button(
        botoes_frame, text="Pesquisar", width=20,
        command=lambda: enviar_saidas(entrada_id_produto, entrada_codigo_barras, tabela)
    ).grid(row=0, column=0, padx=5, pady=5)

    tk.Button(
        botoes_frame, text="Editar Saída", width=20,
        command=lambda: editar_quantidade_motivo(tabela)
    ).grid(row=0, column=1, padx=5, pady=5)

    # Segunda linha de botões
    tk.Button(
        botoes_frame, text="Excluir Produto", width=20,
        command=lambda: excluir_item_tabela(tabela)
    ).grid(row=1, column=0, padx=5, pady=5)

    tk.Button(
    botoes_frame,
    text="Confirmar Saída",
    width=20,
    command=lambda: confirmar_todas_saidas(tabela)
).grid(row=1, column=1, padx=5, pady=5)


    # Botão Sair
    tk.Button(
        janela_atualizar, text="Sair", command=janela_atualizar.destroy,
        width=30
    ).pack(pady=10)
