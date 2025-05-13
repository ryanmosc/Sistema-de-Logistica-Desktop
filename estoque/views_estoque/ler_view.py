import tkinter as tk
from tkinter import ttk, messagebox
from estoque.views_estoque.atualizar_view import exibir_formulario_atualizacao
from estoque.views_estoque.cadastrar_view import exibir_formulario_cadastro
from estoque.functions.deletar import deletar

def exibir_tela_pesquisa(janela):
    from estoque.functions.ler import buscar_produtos
    from saidas.views_saidas.adicionar_saida_views import exibir_formulario_saidas

    for widget in janela.winfo_children():
        widget.destroy()

    janela.title("Pesquisa de Produtos")

    frame_filtros = tk.Frame(janela, pady=10)
    frame_filtros.pack()

    tk.Label(frame_filtros, text="Tipo de Pesquisa:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tipo_pesquisa = ttk.Combobox(frame_filtros, state="readonly", width=20)
    tipo_pesquisa['values'] = ["Tudo", "Por nome", "Por categoria", "Faixa de preço", "Nome + Categoria"]
    tipo_pesquisa.current(0)
    tipo_pesquisa.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_filtros, text="Nome do Produto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_nome = tk.Entry(frame_filtros, width=25)
    entrada_nome.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_filtros, text="Categoria:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    categoria_box = ttk.Combobox(frame_filtros, state="readonly", width=20)
    categoria_box['values'] = ["ALIMENTO", "LIMPEZA", "HIGIENE", "BEBIDAS", "OUTROS", "NULO"]
    categoria_box.current(5)
    categoria_box.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_filtros, text="Preço Mínimo:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    preco_min = tk.Entry(frame_filtros, width=15)
    preco_min.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_filtros, text="Preço Máximo:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    preco_max = tk.Entry(frame_filtros, width=15)
    preco_max.grid(row=2, column=3, padx=5, pady=5)

    def atualizar_campos(*args):
        tipo = tipo_pesquisa.get()

        if tipo == "Por nome":
            entrada_nome.config(state="normal")
            categoria_box.config(state="disabled")
            preco_min.config(state="disabled")
            preco_max.config(state="disabled")

        elif tipo == "Por categoria":
            entrada_nome.config(state="disabled")
            categoria_box.config(state="readonly")
            preco_min.config(state="disabled")
            preco_max.config(state="disabled")

        elif tipo == "Faixa de preço":
            entrada_nome.config(state="disabled")
            categoria_box.config(state="disabled")
            preco_min.config(state="normal")
            preco_max.config(state="normal")

        elif tipo == "Nome + Categoria":
            entrada_nome.config(state="normal")
            categoria_box.config(state="readonly")
            preco_min.config(state="disabled")
            preco_max.config(state="disabled")

        elif tipo == "Tudo":
            entrada_nome.config(state="disabled")
            categoria_box.config(state="readonly")
            preco_min.config(state="disabled")
            preco_max.config(state="disabled")

    def limpar_filtros():
        tipo_pesquisa.current(0)
        entrada_nome.delete(0, tk.END)
        categoria_box.set("NULO")
        preco_min.delete(0, tk.END)
        preco_max.delete(0, tk.END)
        for item in tabela.get_children():
            tabela.delete(item)
        atualizar_campos()

    tipo_pesquisa.bind("<<ComboboxSelected>>", atualizar_campos)
    atualizar_campos()

    frame_botoes = tk.Frame(janela, pady=10)
    frame_botoes.pack()

    tk.Button(frame_botoes, text="🔍 Buscar", width=15,
              command=lambda: buscar_produtos(tipo_pesquisa, entrada_nome, categoria_box, preco_min, preco_max, tabela)
              ).grid(row=0, column=0, padx=10)

    tk.Button(frame_botoes, text="♻️ Limpar Filtros", width=15, command=limpar_filtros).grid(row=0, column=1, padx=10)

    tk.Button(frame_botoes, text="➕ Cadastrar Produto", width=20,
              command=lambda: exibir_formulario_cadastro(janela)).grid(row=0, column=2, padx=10)
    
    def abrir_saidas():
    #     item = tabela.selection()
    #     if not item:
    #         messagebox.showwarning("Aviso", "Selecione um produto para dar baixa.")
    #         return

    #     dados = tabela.item(item[0])['values']
    #     if not dados or len(dados) < 6:
    #         messagebox.showerror("Erro", "Dados incompletos ou inválidos.")
    #         return

        exibir_formulario_saidas(janela)

    def abrir_atualizacao():
        item = tabela.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto para atualizar.")
            return

        dados = tabela.item(item[0])['values']
        if not dados or len(dados) < 6:
            messagebox.showerror("Erro", "Dados incompletos ou inválidos.")
            return

        exibir_formulario_atualizacao(janela, dados)

    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(pady=10)
    
    

    colunas = ("Id", "nome", "estoque", "categoria", "preco_custo", "preco_venda", "data_entrada")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col.replace("_", " ").title())
        tabela.column(col, width=120)
        
    

    tabela.pack()
    
    tk.Button(frame_botoes, text="✏️ Atualizar", width=15, command=abrir_atualizacao).grid(row=0, column=3, padx=10)
    
    tk.Button(frame_botoes, text="🗑️ Deletar", width=15, command=lambda: deletar(tabela)).grid(row=0, column=4, padx=10)
    
    tk.Button(frame_botoes, text=" 📁 Baixas", width=15, command=abrir_saidas).grid(row=0, column=5, padx=10)
    


    
    def voltar_para_home():
        from views.home_view import criar_tela_inicial
        janela.destroy()
        criar_tela_inicial()

    tk.Button(janela, text="Voltar", command=voltar_para_home).pack(pady=5)
    tabela.pack()
