import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from db.conexao import conectar
from entradas.functions.enviar_cadastro_entradas import enviar


def exibir_formulario_entrada(janela_pai):
    janela_entrada = tk.Toplevel(janela_pai)
    janela_entrada.title("Cadastro de Entrada de Produto")
    janela_entrada.geometry("500x550")

    tk.Label(janela_entrada, text="Cadastro de Entrada", font=("Arial", 14, "bold")).pack(pady=10)
    form_frame = tk.Frame(janela_entrada)
    form_frame.pack(pady=10)

    entradas = {}

    categorias_opcoes = ["ALIMENTO", "LIMPEZA", "HIGIENE", "BEBIDAS", "OUTROS"]

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM fornecedores')
    resultado = cursor.fetchall()
    fornecedores = ["NULO"] + [nome[0] for nome in resultado]

    campos = [
        "Nome do Produto",
        "Categoria",
        "Fornecedor",
        "Quantidade",
        "Preço de Custo",
        "Preço de Venda",
        "Data de Entrada",
        "Arquivo XML/PDF"
    ]

    caminho_var = tk.StringVar()

    for idx, campo in enumerate(campos):
        tk.Label(form_frame, text=campo).grid(row=idx, column=0, sticky="e", pady=5, padx=5)

        if campo == "Categoria":
            cb = ttk.Combobox(form_frame, values=categorias_opcoes, state="readonly")
            cb.current(0)
            cb.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = cb

        elif campo == "Fornecedor":
            cb = ttk.Combobox(form_frame, values=fornecedores, state="readonly")
            cb.current(0)
            cb.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = cb

        elif campo == "Data de Entrada":
            de = DateEntry(form_frame, width=19, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            de.set_date(datetime.today())
            de.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = de

        elif campo == "Arquivo XML/PDF":
            frame_arquivo = tk.Frame(form_frame)
            frame_arquivo.grid(row=idx, column=1, pady=5, padx=5, sticky="w")

            entry = tk.Entry(frame_arquivo, textvariable=caminho_var, width=25, state="readonly")
            entry.pack(side="left", padx=5)

            def selecionar_arquivo():
                caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF/XML", "*.pdf *.xml")])
                if caminho:
                    caminho_var.set(caminho)

            tk.Button(frame_arquivo, text="Selecionar", command=selecionar_arquivo).pack(side="left")
            entradas[campo] = caminho_var

        else:
            entry = tk.Entry(form_frame)
            entry.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = entry

    # Botão de envio
    botao_enviar = tk.Button(janela_entrada, text="Enviar", command=lambda: enviar(entradas), bg="green", fg="white", width=20)
    botao_enviar.pack(pady=20)