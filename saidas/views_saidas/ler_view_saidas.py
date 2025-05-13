import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from db.conexao import conectar
from saidas.functions.metricas import gerar_relatorio_opcao

def abrir_tela_saidas(janela):
    from saidas.functions.ler_saidas import buscar_produtos_saidas
    from others.metricas_por_produto import abrir_visao_geral

    for widget in janela.winfo_children():
        widget.destroy()

    janela.title("Controle de Saídas")

    frame_form = tk.Frame(janela, pady=10)
    frame_form.pack()

    frame_filtros = tk.Frame(janela, pady=10)
    frame_filtros.pack()

    tk.Label(frame_filtros, text="Tipo de Pesquisa:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    tipo_pesquisa = ttk.Combobox(frame_filtros, state="readonly", width=25)
    tipo_pesquisa['values'] = [
        "Tudo", "Por nome", "Por categoria", "Nome + Categoria", "Por responsável",
        "Por data", "Por data e categoria", "Por data e nome", "Por data e responsável", "Por data, nome e categoria"
    ]

    tipo_pesquisa.current(0)
    tipo_pesquisa.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_filtros, text="Nome do Produto:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entrada_nome = tk.Entry(frame_filtros, width=25)
    entrada_nome.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame_filtros, text="Motivo:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    categoria_box = ttk.Combobox(frame_filtros, state="readonly", width=25)
    categoria_box['values'] = ["VENDA", "USO INTERNO", "OUTROS", "NULO"]
    categoria_box.current(3)
    categoria_box.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(frame_filtros, text="Responsável:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entrada_responsavel = tk.Entry(frame_filtros, width=25)
    entrada_responsavel.grid(row=2, column=1, padx=5, pady=5)

    # CAMPOS DE DATA
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
        entrada_responsavel.config(state="disabled")
        entrada_data_inicial.config(state="disabled")
        entrada_data_final.config(state="disabled")

        if tipo == "Por nome":
            entrada_nome.config(state="normal")
        elif tipo == "Por categoria":
            categoria_box.config(state="readonly")
        elif tipo == "Nome + Categoria":
            entrada_nome.config(state="normal")
            categoria_box.config(state="readonly")
        elif tipo == "Por responsável":
            entrada_responsavel.config(state="normal")
        elif tipo == "Tudo":
            categoria_box.config(state="readonly")
            entrada_data_inicial.config(state="disabled")
            entrada_data_final.config(state="disabled")

        elif tipo == "Por data":
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")
        elif tipo == "Por data e categoria":
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")
            categoria_box.config(state="readonly")
        elif tipo == "Por data e nome":
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")
            entrada_nome.config(state="normal")
        elif tipo == "Por data e responsável":
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")
            entrada_responsavel.config(state="normal")
        elif tipo == "Por data, nome e categoria":
            entrada_data_inicial.config(state="normal")
            entrada_data_final.config(state="normal")
            entrada_nome.config(state="normal")
            categoria_box.config(state="readonly")

    tipo_pesquisa.bind("<<ComboboxSelected>>", atualizar_campos)
    atualizar_campos()

    # ===== Tabela =====
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(pady=10)

    colunas = ("Id", "nome_produto", "quantidade", "motivo", "responsavel", "data_saida")
    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings")

    for col in colunas:
        tabela.heading(col, text=col.replace("_", " ").title())
        tabela.column(col, width=120)

    tabela.pack()

    def limpar_filtros():
        tipo_pesquisa.current(0)
        entrada_nome.delete(0, tk.END)
        categoria_box.set("NULO")
        entrada_responsavel.delete(0, tk.END)
        entrada_data_inicial.set_date(datetime.today())  # Define a data de hoje
        entrada_data_final.set_date(datetime.today())  # Define a data de hoje
        atualizar_campos()
        for item in tabela.get_children():
            tabela.delete(item)

    # ===== Botões =====
    frame_botoes = tk.Frame(janela, pady=10)
    frame_botoes.pack()

    tk.Button(frame_botoes, text="🔍 Buscar", width=15,
              command=lambda: buscar_produtos_saidas(
                  tipo_pesquisa,
                  entrada_nome,
                  categoria_box,
                  entrada_responsavel,
                  entrada_data_inicial,
                  entrada_data_final,
                  tabela
              )).grid(row=0, column=0, padx=10)

    tk.Button(frame_botoes, text="♻️ Limpar Filtros", width=15, command=limpar_filtros).grid(row=0, column=1, padx=10)

    tk.Button(frame_botoes, text="📄 Gerar Relatório", width=20,
              command=lambda: gerar_relatorio_opcao(tabela)).grid(row=0, column=2, padx=10)

    tk.Button(frame_botoes, text="👁 Visão Geral", width=15,
              command=lambda: abrir_visao_geral(tabela)).grid(row=0, column=3, padx=10)

    def atualizar_tabela():
        for row in tabela.get_children():
            tabela.delete(row)
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT Id, nome_produto, quantidade, motivo, responsavel, data_saida FROM saidas ORDER BY data_saida DESC")
            registros = cursor.fetchall()
            for row in registros:
                tabela.insert("", tk.END, values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar dados: {e}")

    atualizar_tabela()

    def voltar_para_home():
        from views.home_view import criar_tela_inicial
        janela.destroy()
        criar_tela_inicial()

    tk.Button(janela, text="Voltar", command=voltar_para_home).pack(pady=5)
