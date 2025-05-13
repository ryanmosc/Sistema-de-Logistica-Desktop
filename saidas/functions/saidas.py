from db.conexao import conectar
from tkinter import messagebox


def enviar_saidas(entrada_id_produto, entrada_codigo_barras, tabela):
    pesquisa_id = entrada_id_produto.get().strip()
    codigo_barras = entrada_codigo_barras.get().strip()

    try:
        conn = conectar()
        cursor = conn.cursor()

        if codigo_barras:
            cursor.execute('SELECT id, nome_produto, categoria, estoque FROM estoque WHERE id = %s', (codigo_barras,))
        elif pesquisa_id:
            cursor.execute('SELECT id, nome_produto, categoria, estoque FROM estoque WHERE id = %s', (pesquisa_id,))
        else:
            messagebox.showerror("Erro", "Insira o ID ou o Codigo de barras do produto ")  

        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            tabela.insert("", "end", values=resultado)
        
    except Exception :
        messagebox.showerror("Erro", ":Insira o ID ou o Codigo de barras do produto ")
