import tkinter as tk
from tkinter import ttk
from funcionarios.functions.atualizar_funcionarios import enviar_att_funcionario

def exibir_formulario_atualizacao_funcionarios(janela_pai, dados_funcionario):
    janela = tk.Toplevel(janela_pai)
    janela.title("Atualizar Funcionário")
    janela.geometry("500x500")

    tk.Label(janela, text="Atualizar Funcionário", font=("Arial", 14, "bold")).pack(pady=10)
    frame = tk.Frame(janela)
    frame.pack(pady=10)

    entradas = {}
    cargos_opcoes = ["Auxiliar de Estoque", "Supervisor de Logística", "Gerente Operacional", "Estagiário", "OUTROS", "NULO"]

    campos = ["Nome", "Sobrenome", "Cargo", "CPF", "E-mail", "Telefone", "Salário"]

    for idx, campo in enumerate(campos):
        tk.Label(frame, text=campo).grid(row=idx, column=0, sticky="e", pady=5, padx=5)

        if campo == "Cargo":
            box = ttk.Combobox(frame, values=cargos_opcoes, state="readonly")
            box.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = box
        else:
            entry = tk.Entry(frame)
            entry.grid(row=idx, column=1, pady=5, padx=5)
            entradas[campo] = entry

    if dados_funcionario:
        entradas["Nome"].insert(0, dados_funcionario[0])
        entradas["Sobrenome"].insert(0, dados_funcionario[1])
        entradas["Cargo"].set(dados_funcionario[2])
        entradas["CPF"].insert(0, dados_funcionario[3])
        entradas["E-mail"].insert(0, dados_funcionario[4])
        entradas["Telefone"].insert(0, dados_funcionario[5])
        entradas["Salário"].insert(0, str(dados_funcionario[7]))

    tk.Button(
        janela,
        text="Atualizar",
        command=lambda: enviar_att_funcionario(entradas, dados_funcionario)
    ).pack(pady=10)

    tk.Button(janela, text="Fechar", command=janela.destroy).pack()
