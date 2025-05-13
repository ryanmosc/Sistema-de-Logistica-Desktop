from tkinter import messagebox
from db.conexao import conectar

def deletar(tabela):
    item = tabela.selection()
    if not item:
        messagebox.showwarning("Aviso", "Selecione uma entrada para deletar.")
        return

    dados = tabela.item(item[0])["values"]
    id_produto = dados[0]  

    confirmar = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar a entrada ID {id_produto}?")
    if not confirmar:
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entradas WHERE id = %s", (id_produto,))
        conn.commit()
        cursor.close()
        conn.close()

        tabela.delete(item[0])  # Remove da tabela visual
        messagebox.showinfo("Sucesso", f"Produto ID {id_produto} deletado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao deletar o produto: {e}")
