import tkinter as tk
from fornecedores.functions.atualizar import enviar_att_fornecedor


def exibir_formulario_atualizacao_fornecedor(janela_pai, dados_fornecedor):
    janela_atualizar = tk.Toplevel(janela_pai)
    janela_atualizar.title("Atualizar Fornecedor")
    janela_atualizar.geometry("400x400")

    tk.Label(janela_atualizar, text="Atualizar Fornecedor", font=("Arial", 14, "bold")).pack(pady=10)
    form_frame = tk.Frame(janela_atualizar)
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

    # Preenche os dados nos campos
    if dados_fornecedor:
        entradas["Nome"].insert(0, dados_fornecedor[1])
        entradas["CNPJ"].insert(0, dados_fornecedor[2])
        entradas["Telefone"].insert(0, dados_fornecedor[3])
        entradas["Email"].insert(0, dados_fornecedor[4])
        entradas["Endereço"].insert(0, dados_fornecedor[5])

    tk.Button(
        janela_atualizar,
        text="Atualizar",
        command=lambda: enviar_att_fornecedor(entradas, dados_fornecedor[0])
    ).pack(pady=15)

    tk.Button(janela_atualizar, text="Fechar", command=janela_atualizar.destroy).pack(pady=5)
