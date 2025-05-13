from tkinter import messagebox
from db.conexao import conectar

def enviar(entradas):
    try:
        nome = entradas["Nome do Produto"].get().upper().strip()
        estoque = int(entradas["Estoque"].get())
        categoria = entradas["Categoria"].get()
        preco_custo = float(entradas["Preço de Custo"].get())
        preco_venda = float(entradas["Preço de Venda"].get())
        
        if not nome:
            messagebox.showerror("Erro", "O campo 'Nome do produto' não pode estar vazio.")
        elif estoque < 0:
            messagebox.showerror("Erro", "O valor de estoque não pode ser negativo.")

        else:

            conn = conectar()
            cursor = conn.cursor()
            

            cursor.execute("""
                INSERT INTO estoque (nome_produto, estoque, categoria, preco_custo, preco_venda, data_entrada)
                VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
            """, (nome, estoque, categoria, preco_custo, preco_venda))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

            for campo in entradas.values():
                campo.delete(0, "end")

    except ValueError:
        messagebox.showerror("Erro", "Verifique os campos numéricos. Use '.' para decimais.")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
