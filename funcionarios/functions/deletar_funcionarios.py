from tkinter import messagebox
from db.conexao import conectar

def deletar_funcionarios(tabela):
    item = tabela.selection()
    if not item:
        messagebox.showwarning("Aviso", "Selecione um funcionario para deletar.")
        return

    dados = tabela.item(item[0])["values"]
    cpf = dados[3]  
    nome = dados [0]

    confirmar = messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar o funcionario {nome}?")
    if not confirmar:
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM funcionarios WHERE cpf ='%s' ", (cpf,))
        conn.commit()
        cursor.close()
        conn.close()

        tabela.delete(item[0])  
        messagebox.showinfo("Sucesso", f"funcionario {nome} deletado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao deletar o funcionario: {e}")
