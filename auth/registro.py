import bcrypt
import re
from tkinter import messagebox
from db.conexao import conectar

#Funçoês para registro de usuarios no sistema (Pode ser alterado para dentro do codigo para apenas pessoas com o cargo de ADM ou + poderem adicionar)
def registrar_usuario(nome, usuario, senha,repet,email):
    if not nome.strip():
        messagebox.showerror("Erro", "O nome não pode estar vazio!")
        return

    if not usuario.strip():
        messagebox.showerror("Erro", "O nome de usuário não pode estar vazio!")
        return
    
    #Validação de E-mail
    if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            messagebox.showerror("Erro", "Email inválido! Use um formato válido (ex.: usuario@dominio.com)")
            return 
    
    #So avança se ambas as senhas forem iguais
    if senha != repet:
        messagebox.showerror("Erro", "As senhas devem ser iguais!")
        
    #A senha deve ser maior que 8
    if len(senha) < 8:
        messagebox.showerror("Erro", "A senha precisa ter pelo menos 8 caracteres!")
        return

    conexao = conectar()
    if not conexao:
        return

    #Tratamento com banco de dados e inserção de dados
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
        if cursor.fetchone():
            messagebox.showerror("Erro", "Este usuário já está cadastrado!")
            return

        senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


        cursor.execute("""
            INSERT INTO usuarios (nomes, usuario, senhas,email)
            VALUES (%s, %s, %s,%s)
        """, (nome, usuario, senha_criptografada,email))

        conexao.commit()
        messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")

    finally:
        cursor.close()
        conexao.close()
