import tkinter as tk
from tkinter import ttk, messagebox


def exibir_tela_pesquisa_fornecedores(janela):
    from fornecedores.fornecedores_view.cadastrar_view_fornecedores import exibir_formulario_fornecedor
    from fornecedores.functions.ler_fornecedores import buscar_produtos
    from fornecedores.functions.deletar import deletar
    from fornecedores.fornecedores_view.atualizar_view_fornecedores import exibir_formulario_atualizacao_fornecedor



    for widget in janela.winfo_children():
        widget.destroy()

    janela.title("Pesquisa de Fornecedores")

    frame_filtros = tk.Frame(janela, pady=10)
    frame_filtros.pack()

    tk.Label(frame_filtros, text="Tipo de Pesquisa:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tipo_pesquisa = ttk.Combobox(frame_filtros, state="readonly", width=20)
    tipo_pesquisa['values'] = ["Tudo", "Por nome", "Por cnpj"]
    tipo_pesquisa.current(0)
    tipo_pesquisa.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_filtros, text="Nome do Fornecedor:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_nome = tk.Entry(frame_filtros, width=25)
    entrada_nome.grid(row=1, column=1, padx=5, pady=5)



    tk.Label(frame_filtros, text="Por Cnpj:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    por_cnpj = tk.Entry(frame_filtros, width=15)
    por_cnpj.grid(row=2, column=3, padx=5, pady=5)

    def atualizar_campos(*args):
        tipo = tipo_pesquisa.get()

        if tipo == "Por nome":
            entrada_nome.config(state="normal")
            por_cnpj.config(state="disabled")

        elif tipo == "Por cnpj":
            por_cnpj.config(state="normal")
            entrada_nome.config(state="disabled")

        

    def limpar_filtros():
        tipo_pesquisa.current(0)
        entrada_nome.delete(0, tk.END)
        
        por_cnpj.delete(0, tk.END)
        entrada_nome.delete(0, tk.END)
        for item in tabela.get_children():
            tabela.delete(item)
        atualizar_campos()

    tipo_pesquisa.bind("<<ComboboxSelected>>", atualizar_campos)
    atualizar_campos()

    frame_botoes = tk.Frame(janela, pady=10)
    frame_botoes.pack()

    tk.Button(frame_botoes, text="🔍 Buscar", width=15,
              command=lambda: buscar_produtos(tipo_pesquisa, entrada_nome, por_cnpj, tabela)
              ).grid(row=0, column=0, padx=10)

    tk.Button(frame_botoes, text="♻️ Limpar Filtros", width=15, command=limpar_filtros).grid(row=0, column=1, padx=10)

    tk.Button(frame_botoes, text="➕ Cadastrar Fornecedor", width=20,
              command=lambda: exibir_formulario_fornecedor(janela)).grid(row=0, column=2, padx=10)
    
 

   
    
    
    
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(pady=10)

    colunas = ("Id", "nome", "cnpj", "telefone", "email", "endereco", "data_cadastro")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col.replace("_", " ").title())
        tabela.column(col, width=120)
        
    

    tabela.pack()
    
    def abrir_formulario_atualizacao(tabela, janela_pai):
            selecionado = tabela.selection()
            if not selecionado:
                messagebox.showerror("Erro", "Selecione um fornecedor para atualizar!")
                return
            item = tabela.item(selecionado[0])
            dados_fornecedor = item['values']
            exibir_formulario_atualizacao_fornecedor(janela_pai, dados_fornecedor)

    tk.Button(
        frame_botoes,
        text="✏️ Atualizar",
        width=15,
        command=lambda: abrir_formulario_atualizacao(tabela, janela)
    ).grid(row=0, column=3, padx=10)
    
    tk.Button(frame_botoes, text="🗑️ Deletar", width=15, command=lambda: deletar(tabela)).grid(row=0, column=4, padx=10)
    
  
    


    
    def voltar_para_home():
        from views.home_view import criar_tela_inicial
        janela.destroy()
        criar_tela_inicial()

    tk.Button(janela, text="Voltar", command=voltar_para_home).pack(pady=5)
    tabela.pack()
