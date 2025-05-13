from tkinter import messagebox
from db.conexao import conectar
import re

def enviar_fornecedores(entradas):
    try:
        nome = entradas["Nome"].get().upper().strip()
        cnpj = re.sub(r'\D', '', entradas["CNPJ"].get()) 
        telefone = entradas["Telefone"].get().strip()
        email = entradas["Email"].get().strip()
        endereco = entradas["Endereço"].get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "O campo 'Nome' não pode estar vazio.")
        
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            messagebox.showerror("Erro", "Email inválido! Use um formato válido (ex.: usuario@dominio.com)")
            return 
        

        else:

            conn = conectar()
            cursor = conn.cursor()
            

            cursor.execute("""
                INSERT INTO fornecedores (nome, cnpj, telefone, email, endereco, data_cadastro)
                VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
            """, (nome, cnpj, telefone, email, endereco))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")

            for campo in entradas.values():
                campo.delete(0, "end")

    except ValueError:
        messagebox.showerror("Erro", "Verifique os campos numéricos. Use '.' para decimais.")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
