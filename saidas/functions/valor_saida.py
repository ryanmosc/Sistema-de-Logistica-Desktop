import tkinter as tk
from tkinter import ttk, messagebox

def editar_quantidade_motivo(tabela):
    item_selecionado = tabela.selection()
    if not item_selecionado:
        messagebox.showwarning("Nenhum item", "Selecione um produto na tabela.")
        return

    item = item_selecionado[0]
    valores = tabela.item(item, "values")

    janela_editar = tk.Toplevel()
    janela_editar.title("Editar Saída")
    janela_editar.geometry("300x250")

    tk.Label(janela_editar, text=f"Produto: {valores[1]}", font=("Arial", 12, "bold")).pack(pady=10)

    # Campo para quantidade
    tk.Label(janela_editar, text="Quantidade de Saída:").pack()
    entrada_quantidade = tk.Entry(janela_editar)
    entrada_quantidade.pack(pady=5)

    # Combobox para motivo
    tk.Label(janela_editar, text="Motivo da Saída:").pack()
    opcoes_motivo = ["Venda", "Devolução", "Perda", "Troca", "Outros"]
    combo_motivo = ttk.Combobox(janela_editar, values=opcoes_motivo, state="readonly")
    combo_motivo.pack(pady=5)

    def salvar():
        quantidade = entrada_quantidade.get().strip()
        motivo = combo_motivo.get().strip()

        if not quantidade.isdigit():
            messagebox.showerror("Erro", "Insira uma quantidade válida.")
            return
        if not motivo:
            messagebox.showerror("Erro", "Selecione um motivo.")
            return

        # Atualizar valores na tabela
        novo_valor = (valores[0], valores[1], valores[2], valores[3], quantidade, motivo)
        tabela.item(item, values=novo_valor)
        janela_editar.destroy()

    tk.Button(janela_editar, text="Salvar", command=salvar).pack(pady=10)
