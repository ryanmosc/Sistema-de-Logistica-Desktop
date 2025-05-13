from tkinter import messagebox


def excluir_item_tabela(tabela):
   
        item_selecionado = tabela.selection()
        if item_selecionado:
            for item in item_selecionado:
                tabela.delete(item)
        else:
            messagebox.showerror("Erro","Selecione um produto para deletar")
    
    

