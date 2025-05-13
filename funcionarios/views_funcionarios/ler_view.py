import tkinter as tk
from tkinter import ttk, messagebox
from funcionarios.views_funcionarios.cadastrar_view import exibir_formulario_funcionario
from funcionarios.functions.ler import buscar_funcionarios
from funcionarios.views_funcionarios.atualizar_view_funcionarios import exibir_formulario_atualizacao_funcionarios
from funcionarios.functions.deletar_funcionarios import deletar_funcionarios


def exibir_tela_funcionarios(janela):
    for widget in janela.winfo_children():
        widget.destroy()

    janela.title("Pesquisa de Funcionários")

    frame_filtros = tk.Frame(janela, pady=10)
    frame_filtros.pack()

    # Tipo de pesquisa
    tk.Label(frame_filtros, text="Tipo de Pesquisa:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tipo_pesquisa = ttk.Combobox(frame_filtros, state="readonly", width=20)
    tipo_pesquisa['values'] = ["Tudo", "Por nome", "Por cargo", "CPF"]
    tipo_pesquisa.current(0)
    tipo_pesquisa.grid(row=0, column=1, padx=5, pady=5)

    # Nome
    tk.Label(frame_filtros, text="Nome do Funcionário:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_nome = tk.Entry(frame_filtros, width=25)
    entrada_nome.grid(row=1, column=1, padx=5, pady=5)

    # Cargo
    tk.Label(frame_filtros, text="Cargo:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    cargo_box = ttk.Combobox(frame_filtros, state="readonly", width=20)
    cargo_box['values'] = ["Auxiliar de Estoque", "Supervisor de Logística", "Gerente Operacional", "Estagiário", "OUTROS", "NULO"]
    cargo_box.current(5)
    cargo_box.grid(row=1, column=3, padx=5, pady=5)

    # CPF
    tk.Label(frame_filtros, text="CPF:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entrada_cpf = tk.Entry(frame_filtros, width=25)
    entrada_cpf.grid(row=2, column=1, padx=5, pady=5)

    # Atualiza campos com base no tipo de pesquisa
    def atualizar_campos(*args):
        tipo = tipo_pesquisa.get()
        entrada_nome.config(state="disabled")
        cargo_box.config(state="disabled")
        entrada_cpf.config(state="disabled")

        if tipo == "Por nome":
            entrada_nome.config(state="normal")
        elif tipo == "Por cargo":
            cargo_box.config(state="readonly")
        elif tipo == "CPF":
            entrada_cpf.config(state="normal")
        elif tipo == "Tudo":
            cargo_box.config(state="readonly")

    tipo_pesquisa.bind("<<ComboboxSelected>>", atualizar_campos)
    atualizar_campos()

    def limpar_filtros():
        tipo_pesquisa.current(0)
        entrada_nome.delete(0, tk.END)
        entrada_cpf.delete(0, tk.END)
        cargo_box.set("NULO")
        atualizar_campos()
        for item in tabela.get_children():
            tabela.delete(item)

    # Botões
    frame_botoes = tk.Frame(janela, pady=10)
    frame_botoes.pack()

    tk.Button(frame_botoes, text="🔍 Buscar", width=15,
              command=lambda: buscar_funcionarios(tipo_pesquisa, entrada_nome, cargo_box, entrada_cpf, tabela)
              ).grid(row=0, column=0, padx=10)

    tk.Button(frame_botoes, text="♻️ Limpar Filtros", width=15, command=limpar_filtros).grid(row=0, column=1, padx=10)

    tk.Button(frame_botoes, text="➕ Cadastrar Funcionário", width=20,
              command=lambda: exibir_formulario_funcionario(janela)).grid(row=0, column=2, padx=10)

    # Tabela
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(pady=10)

    colunas = ("Nome", "Sobrenome", "Cargo", "CPF", "E-mail", "Telefone", "Data_Admissao", "Salario")
    global tabela  
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col.replace("_", " ").title())
        tabela.column(col, width=120)
    def voltar_para_home():
        from views.home_view import criar_tela_inicial
        janela.destroy()
        criar_tela_inicial()

    tk.Button(janela, text="Voltar", command=voltar_para_home).pack(pady=5)
    tabela.pack()
    
    def abrir_formulario_atualizacao():
        item_selecionado = tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Seleção necessária", "Selecione um funcionário para atualizar.")
            return

        dados = tabela.item(item_selecionado)["values"]
        exibir_formulario_atualizacao_funcionarios(janela, dados)

    tk.Button(frame_botoes, text="✏️ Atualizar", width=15, command=abrir_formulario_atualizacao).grid(row=0, column=3, padx=10)
    tk.Button(frame_botoes, text="🗑️ Deletar", width=15, command=lambda: deletar_funcionarios(tabela)).grid(row=0, column=4, padx=10)
    