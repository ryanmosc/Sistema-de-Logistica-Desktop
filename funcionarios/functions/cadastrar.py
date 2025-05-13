from tkinter import messagebox
from db.conexao import conectar
import re

#COLOCAR VALIDAÇÃO DE CPF E EMAIL E N TELEFONE

def enviar_funcionario(entradas):
    try:
        nome = entradas["Nome"].get().strip().upper()
        last_name = entradas["Sobrenome"].get().strip().upper()
        cargo = entradas["Cargo"].get()
        cpf = entradas["CPF"].get().strip()
        salario = float(entradas["Salário"].get())
        email = entradas["E-mail"].get().strip().upper()
        telefone = entradas["Telefone"].get().strip()

        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            messagebox.showerror("Erro", "Email inválido! Use um formato válido (ex.: usuario@dominio.com)")
            return
        
        if not nome or not last_name or not cpf:
            messagebox.showerror("Erro", "Nome, sobrenome e CPF são obrigatórios.")
            return
        elif salario < 0:
            messagebox.showerror("Erro", "O salário não pode ser negativo.")
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
    INSERT INTO funcionarios (nome, last_name, cargo, cpf, salario, email, telefone, data_admissao)
    VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_DATE)
    """, (nome, last_name, cargo, cpf, salario, email, telefone))


        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")

        for campo in entradas.values():
            campo.delete(0, "end")

    except ValueError:
        messagebox.showerror("Erro", "Verifique os campos numéricos. Use '.' para decimais.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
