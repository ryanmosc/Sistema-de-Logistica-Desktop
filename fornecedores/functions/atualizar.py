from tkinter import messagebox
from db.conexao import conectar
import re

def enviar_att_fornecedor(entradas, id_atualizado):
    try:
        nome = entradas["Nome"].get().strip().upper()
        cnpj = re.sub(r'\D', '', entradas["CNPJ"].get()) 
        telefone = entradas["Telefone"].get().strip()
        email = entradas["Email"].get().strip()
        endereco = entradas["Endereço"].get().strip()

        if not nome:
            messagebox.showerror("Erro", "O campo 'Nome' não pode estar vazio.")
            return
        if not cnpj:
            messagebox.showerror("Erro", "O campo 'CNPJ' não pode estar vazio.")

        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            messagebox.showerror("Erro", "Email inválido! Use um formato válido (ex.: usuario@dominio.com)")
            return 
            

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE fornecedores
            SET nome = %s,
                cnpj = %s,
                telefone = %s,
                email = %s,
                endereco = %s
            WHERE id = %s
        """, (nome, cnpj, telefone, email, endereco, id_atualizado))

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso!")

        for campo in entradas.values():
            campo.delete(0, "end")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
