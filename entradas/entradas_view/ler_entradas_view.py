import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from db.conexao import conectar
import os
import platform
import subprocess

def exibir_entradas(janela):
    from entradas.functions.ler_entradas import buscar_produtos
    from entradas.entradas_view.cadastrar_entradas import exibir_formulario_entrada
    from entradas.functions.deletar import deletar
    from entradas.entradas_view.atualizar_entradas import exibir_formulario_atualizacao_entrada

    for widget in janela.winfo_children():
        widget.destroy()

    janela.title("Pesquisa de Entradas")

    # Frame de Filtros
    frame_filtros = tk.Frame(janela, pady=10)
    frame_filtros.pack()

    tk.Label(frame_filtros, text="Tipo de Pesquisa:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tipo_pesquisa = ttk.Combobox(frame_filtros, state="readonly", width=25)
    tipo_pesquisa['values'] = [
        "Tudo", "Por nome", "Por categoria", "Por fornecedor", "Nome + Categoria", 
        "Por data", "Por data e categoria", "Por data e nome", 
        "Por data e responsável", "Por data, nome e categoria"
    ]
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

    tk.Label(frame_filtros, text="Fornecedor:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM fornecedores')
    resultado = cursor.fetchall()
    fornecedores = ["NULO"] + [nome[0] for nome in resultado]
    entrada_nome_fornecedor = ttk.Combobox(frame_filtros, values=fornecedores, state="readonly", width=25)
    entrada_nome_fornecedor.current(0)
    entrada_nome_fornecedor.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_filtros, text="Data Inicial:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
    entrada_data_inicial = DateEntry(frame_filtros, width=22, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    entrada_data_inicial.grid(row=2, column=3, padx=5, pady=5)

    tk.Label(frame_filtros, text="Data Final:").grid(row=3, column=2, padx=5, pady=5, sticky="e")
    entrada_data_final = DateEntry(frame_filtros, width=22, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    entrada_data_final.grid(row=3, column=3, padx=5, pady=5)

    def atualizar_campos(*args):
        tipo = tipo_pesquisa.get()
        entrada_nome.config(state="disabled")
        categoria_box.config(state="disabled")
        entrada_nome_fornecedor.config(state="disabled")
        entrada_data_inicial.config(state="disabled")
        entrada_data_final.config(state="disabled")

        if tipo == "Por nome":
            entrada_nome.config(state="normal")
        elif tipo == "Por categoria":
            categoria_box.config(state="normal")
        elif tipo == "Por fornecedor":
            entrada_nome_fornecedor.config(state="normal")
        elif tipo == "Nome + Categoria":
            entrada_nome.config(state="normal")
            categoria_box.config(state="normal")
        elif tipo == "Por data":
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")
        elif tipo == "Por data e categoria":
            categoria_box.config(state="normal")
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")
        elif tipo == "Por data e nome":
            entrada_nome.config(state="normal")
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")
        elif tipo == "Por data e responsável":
            entrada_nome_fornecedor.config(state="normal")
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")
        elif tipo == "Por data, nome e categoria":
            entrada_nome.config(state="normal")
            categoria_box.config(state="normal")
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")

    tipo_pesquisa.bind("<<ComboboxSelected>>", atualizar_campos)
    atualizar_campos()

    def limpar_filtros():
        tipo_pesquisa.current(0)
        entrada_nome.delete(0, tk.END)
        categoria_box.set("NULO")
        if fornecedores:
            entrada_nome_fornecedor.set(fornecedores[0])
        entrada_data_inicial.set_date(datetime.today())
        entrada_data_final.set_date(datetime.today())
        atualizar_campos()
        for item in tabela.get_children():
            tabela.delete(item)

    # Frame de Botões
    frame_botoes = tk.Frame(janela, pady=10)
    frame_botoes.pack()

    tk.Button(frame_botoes, text="🔍 Buscar", width=15,
              command=lambda: buscar_produtos(tipo_pesquisa, entrada_nome, categoria_box,
                                              entrada_data_inicial, entrada_data_final,
                                              entrada_nome_fornecedor, tabela)).grid(row=0, column=0, padx=10)

    tk.Button(frame_botoes, text="♻️ Limpar Filtros", width=15, command=limpar_filtros).grid(row=0, column=1, padx=10)

    tk.Button(frame_botoes, text="➕ Cadastrar Entrada", width=20,
              command=lambda: exibir_formulario_entrada(janela)).grid(row=0, column=2, padx=10)

    def atualizar_entrada_selecionada():
        item_selecionado = tabela.selection()
        valores = tabela.item(item_selecionado)["values"]
        id_entrada = valores[0]
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma entrada para atualizar.")
            return
        dados_entrada = tabela.item(item_selecionado)["values"]
        exibir_formulario_atualizacao_entrada(janela, dados_entrada,id_entrada)

  
    
    tk.Button(frame_botoes, text="✏️ Atualizar", width=15, command=atualizar_entrada_selecionada).grid(row=0, column=3, padx=10)
    tk.Button(frame_botoes, text="🗑️ Deletar", width=15, command=lambda: deletar(tabela)).grid(row=0, column=4, padx=10)

    def abrir_arquivo_selecionado():
        item_selecionado = tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma entrada para abrir o arquivo.")
            return
        valores = tabela.item(item_selecionado)["values"]
        id_entrada = valores[0]
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT nome, conteudo FROM arquivos WHERE id_entrada = %s", (id_entrada,))
            resultado = cur.fetchone()
            if not resultado:
                messagebox.showwarning("Aviso", "Nenhum arquivo encontrado para esta entrada.")
                return
            nome, conteudo = resultado
            caminho_temp = os.path.join(os.getcwd(), nome)
            with open(caminho_temp, "wb") as f:
                f.write(conteudo)

            if platform.system() == "Windows":
                os.startfile(caminho_temp)
            elif platform.system() == "Darwin":
                subprocess.call(("open", caminho_temp))
            else:
                subprocess.call(("xdg-open", caminho_temp))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir o arquivo: {e}")
        finally:
            cur.close()
            conn.close()

    tk.Button(frame_botoes, text="📂 Abrir Arquivo", width=15, command=abrir_arquivo_selecionado).grid(row=0, column=5, padx=10)

    # Tabela
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(pady=10)

    colunas = ("Id", "nome_produto", "fornecedor", "quantidade", "preco_custo", "preco_venda",
               "data_entrada", "arquivo_xml_pdf")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col.replace("_", " ").title())
        tabela.column(col, width=120)

    tabela.pack()

    def voltar_para_home():
        from views.home_view import criar_tela_inicial
        janela.destroy()
        criar_tela_inicial()

    tk.Button(janela, text="Voltar", command=voltar_para_home).pack(pady=5)
