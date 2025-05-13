from tkinter import messagebox
from db.conexao import conectar
from others.enviar_email import enviar_email
import openpyxl
import fpdf
import pandas as pd

def verificar_estoque_baixo():
    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT nome_produto, estoque FROM estoque WHERE estoque <= 5")
        produtos = cursor.fetchall()

        if produtos:
            alerta = "Produtos com estoque baixo:\n\n"
            for nome, estoque in produtos:
                alerta += f" {nome}: {estoque} unidades\n"

           
            df = pd.DataFrame(produtos, columns=["Produto", "Estoque"])
            arquivo_excel = 'relatorio_ventas.xlsx'
            df.to_excel(arquivo_excel, index=False)

            
            enviar_email(arquivo_excel)

              


            messagebox.showwarning("Estoque Baixo", alerta)
            df = pd.DataFrame(produtos, columns=["Produto", "Estoque"])
            arquivo_excel = 'relatorio_ventas.xlsx'
            df.to_excel(arquivo_excel, index=False)

            
            enviar_email(arquivo_excel)
        else:
            messagebox.showinfo("Estoque Ok", "Nenhum produto com estoque baixo encontrado.")

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao verificar estoque: {e}")
