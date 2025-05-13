from tkinter import messagebox
from db.conexao import conectar

def enviar_att(entradas, id_atualizado):
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
                UPDATE estoque
                SET nome_produto = %s,
                    estoque = %s,
                    categoria = %s,
                    preco_custo = %s,
                    preco_venda = %s,
                    data_entrada = CURRENT_DATE
                WHERE id = %s
            """, (nome, estoque, categoria, preco_custo, preco_venda, id_atualizado))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")

            for campo in entradas.values():
                campo.delete(0, "end")

    except ValueError:
        messagebox.showerror("Erro", "Verifique os campos numéricos. Use '.' para decimais.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
