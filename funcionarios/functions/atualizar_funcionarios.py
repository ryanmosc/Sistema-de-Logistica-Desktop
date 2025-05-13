from tkinter import messagebox
from db.conexao import conectar
import re

def enviar_att_funcionario(entradas, dados_funcionario):
    try:
        nome = entradas["Nome"].get().strip().upper()
        sobrenome = entradas["Sobrenome"].get().strip().upper()
        cargo = entradas["Cargo"].get()
        cpf = entradas["CPF"].get().strip()
        email = entradas["E-mail"].get().strip().upper()
        telefone = entradas["Telefone"].get().strip()
        salario = float(entradas["Salário"].get())

        if not nome or not sobrenome or not cpf:
            messagebox.showerror("Erro", "Nome, sobrenome e CPF são obrigatórios.")
            return
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            messagebox.showerror("Erro", "Email inválido! Use um formato válido (ex.: usuario@dominio.com)")
            return
        
        if salario < 0:
            messagebox.showerror("Erro", "O salário não pode ser negativo.")
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE funcionarios
            SET nome=%s, last_name=%s, cargo=%s, cpf=%s, email=%s, telefone=%s, salario=%s
            WHERE cpf='%s'
        """, (nome, sobrenome, cargo, cpf, email, telefone, salario, dados_funcionario[3]))

        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")

    except ValueError:
        messagebox.showerror("Erro", "Salário inválido. Use ponto (.) como separador decimal.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar funcionário: {e}")
