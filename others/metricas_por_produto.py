import tkinter as tk
from tkinter import messagebox, Toplevel
from db.conexao import conectar

def abrir_visao_geral(tabela):
    selecionado = tabela.focus()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um produto na tabela primeiro!")
        return

    produto = tabela.item(selecionado, "values")[1]  
    if not produto:
        messagebox.showerror("Erro", "Produto não encontrado na seleção.")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()

     
        cursor.execute('SELECT SUM(quantidade) FROM saidas WHERE nome_produto = %s', (produto,))
        total_geral = cursor.fetchone()[0] or 0

        cursor.execute('SELECT SUM(quantidade) FROM saidas WHERE nome_produto = %s AND motivo = %s', (produto, 'VENDA'))
        venda = cursor.fetchone()[0] or 0

        cursor.execute('SELECT SUM(quantidade) FROM saidas WHERE nome_produto = %s AND motivo = %s', (produto, 'USO INTERNO'))
        interno = cursor.fetchone()[0] or 0

        cursor.execute('SELECT SUM(quantidade) FROM saidas WHERE nome_produto = %s AND motivo = %s', (produto, 'OUTRO'))
        outros = cursor.fetchone()[0] or 0

        cursor.close()
        conn.close()

        # Criar nova janela
        janela_geral = Toplevel()
        janela_geral.title(f"Visão Geral - {produto}")
        janela_geral.geometry("300x250")

        info = f"""
Produto: {produto}

Total Geral de Saídas: {total_geral}

▶ Vendas: {venda}
▶ Uso Interno: {interno}
▶ Outros: {outros}
"""

        label_info = tk.Label(janela_geral, text=info, justify="left", font=("Arial", 10))
        label_info.pack(pady=10, padx=10)

        tk.Button(janela_geral, text="Fechar", command=janela_geral.destroy).pack(pady=5)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar visão geral: {e}")
