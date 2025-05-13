import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from fpdf import FPDF


def gerar_xls(dados, colunas):
    df = pd.DataFrame(dados, columns=colunas)
    caminho = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Arquivo Excel (*.xlsx)", "*.xlsx")],
        title="Salvar como Excel"
    )
    if caminho:
        df.to_excel(caminho, index=False)
        messagebox.showinfo("Sucesso", f"Relatório salvo com sucesso:\n{caminho}")


def gerar_pdf(dados, colunas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    # Largura das colunas (dividido igualmente)
    largura_pagina = 190  
    larguras = [largura_pagina // len(colunas)] * len(colunas)

    # Cabeçalho
    for i, col in enumerate(colunas):
        pdf.cell(larguras[i], 10, col, border=1, align="C")
    pdf.ln()

    # Dados
    for linha in dados:
        for i, item in enumerate(linha):
            pdf.cell(larguras[i], 10, str(item), border=1)
        pdf.ln()

    caminho = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivo PDF (*.pdf)", "*.pdf")],
        title="Salvar como PDF"
    )
    if caminho:
        pdf.output(caminho)
        messagebox.showinfo("Sucesso", f"Relatório salvo com sucesso:\n{caminho}")


def gerar_relatorio_opcao(tabela):
    itens = tabela.get_children()
    if not itens:
        messagebox.showwarning("Atenção", "Nenhum dado encontrado para gerar relatório.")
        return

    dados = [tabela.item(item)['values'] for item in itens]
    colunas = [tabela.heading(col)['text'] for col in tabela['columns']]

    janela_opcao = tk.Toplevel()
    janela_opcao.title("Gerar Relatório")
    janela_opcao.geometry("300x200")
    janela_opcao.resizable(False, False)
    janela_opcao.configure(bg="#f5f5f5")

    tk.Label(
        janela_opcao,
        text="Selecione o formato do relatório:",
        font=("Arial", 12, "bold"),
        bg="#f5f5f5",
        fg="#2c3e50"
    ).pack(pady=20)

    tk.Button(
        janela_opcao,
        text="📄 Gerar PDF",
        width=20,
        command=lambda: [gerar_pdf(dados, colunas), janela_opcao.destroy()]
    ).pack(pady=10)

    tk.Button(
        janela_opcao,
        text="📊 Gerar Excel",
        width=20,
        command=lambda: [gerar_xls(dados, colunas), janela_opcao.destroy()]
    ).pack(pady=10)


