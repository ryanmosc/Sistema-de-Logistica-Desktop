import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry
from db.conexao import conectar
import datetime
import os
import subprocess
import tempfile

def exibir_formulario_atualizacao_entrada(janela_pai, dados_entrada,id_entrada):
    janela_atualizar = tk.Toplevel(janela_pai)
    janela_atualizar.title("Atualizar Entrada de Produto")
    janela_atualizar.geometry("500x650")

    tk.Label(janela_atualizar, text="Atualizar Entrada", font=("Arial", 14, "bold")).pack(pady=10)
    form_frame = tk.Frame(janela_atualizar)
    form_frame.pack(pady=10)

    entradas = {}

    # Buscar fornecedores
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM fornecedores')
    resultado = cursor.fetchall()
    fornecedores = ["NULO"] + [nome[0] for nome in resultado]
    cursor.close()
    conn.close()

    campos = [
        ("Nome do Produto", tk.Entry),
        ("Categoria", ttk.Combobox),
        ("Fornecedor", ttk.Combobox),
        ("Quantidade", tk.Entry),
        ("Preço de Custo", tk.Entry),
        ("Preço de Venda", tk.Entry),
        ("Data de Entrada", DateEntry),
        ("Arquivo XML/PDF", tk.Entry)
    ]

    for idx, (campo, widget) in enumerate(campos):
        tk.Label(form_frame, text=campo).grid(row=idx, column=0, sticky="e", pady=5, padx=5)

        if campo == "Categoria":
            entrada = widget(form_frame, values=["ALIMENTO", "LIMPEZA", "HIGIENE", "BEBIDAS", "OUTROS"], state="readonly")
        elif campo == "Fornecedor":
            entrada = widget(form_frame, values=fornecedores, state="readonly")
        elif widget == DateEntry:
            entrada = widget(form_frame, date_pattern="yyyy-mm-dd")
        else:
            entrada = widget(form_frame)

        entrada.grid(row=idx, column=1, pady=5, padx=5, sticky="we")
        entradas[campo] = entrada

    # Abrir arquivo
    def abrir_arquivo_selecionado():
        import platform
        
       
        
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
        
    # Selecionar novo arquivo
    def selecionar_arquivo():
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF/XML", "*.pdf *.xml")])
        if caminho:
            entradas["Arquivo XML/PDF"].delete(0, tk.END)
            entradas["Arquivo XML/PDF"].insert(0, caminho)

    # Botões de arquivo
    tk.Button(form_frame, text="Selecionar Arquivo", command=selecionar_arquivo).grid(row=7, column=2, padx=5, pady=5)
    tk.Button(form_frame, text="Abrir Arquivo", command=abrir_arquivo_selecionado).grid(row=7, column=3, padx=5, pady=5)

    # Preenche os campos
    if dados_entrada:
        entradas["Nome do Produto"].insert(0, dados_entrada[1])
        entradas["Fornecedor"].set(dados_entrada[2])
        entradas["Quantidade"].insert(0, str(dados_entrada[3]))
        entradas["Preço de Custo"].insert(0, str(dados_entrada[4]))
        entradas["Preço de Venda"].insert(0, str(dados_entrada[5]))

        try:
            data = dados_entrada[6]
            if isinstance(data, memoryview):
                data = data.tobytes().decode('utf-8')
            data = str(data).split(" ")[0]
            data_formatada = datetime.datetime.strptime(data, "%Y-%m-%d").date()
            entradas["Data de Entrada"].set_date(data_formatada)
        except Exception as e:
            messagebox.showerror("Erro de Data", f"Erro ao converter data: {e}")
        cursor.execute('SELECT nome FROM arquivos WHERE id_entrada = %s',(id_entrada,))
        nome_arquivo = cursor.fetchone()
        entradas["Arquivo XML/PDF"].insert(0, nome_arquivo[0] if nome_arquivo else "")


    # Botões finais
    tk.Button(
        janela_atualizar,
        text="Atualizar",
        command=lambda: print("Função de atualização vai aqui")
    ).pack(pady=15)

    tk.Button(janela_atualizar, text="Fechar", command=janela_atualizar.destroy).pack(pady=5)
