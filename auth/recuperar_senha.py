
import bcrypt
from tkinter import messagebox
from db.conexao import conectar  

def recuperar_senha( email, nova_senha,repet_nova_senha):
    if not email or not nova_senha or not repet_nova_senha:
        messagebox.showerror("Erro", "E-mail e nova senha são obrigatórios!")
        return False
    
    if nova_senha != repet_nova_senha:
            messagebox.showerror("Erro", "As senhas devem ser iguais!")
            return False

    if len(repet_nova_senha ) < 8:
        messagebox.showerror("Erro", "A senha precisa ter pelo menos 8 caracteres!")
        return False

    try:
        conexao = conectar()
        cursor = conexao.cursor()

       
        cursor.execute("SELECT usuario FROM usuarios WHERE email = %s", (email,))
        resultado = cursor.fetchone()

        if not resultado:
            messagebox.showerror("Erro", "E-mail incorreto ou invalido.")
            return False
        
        senha_criptografada = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        
        
        
        cursor.execute(
            "UPDATE usuarios SET senhas = %s WHERE  email = %s",
            (senha_criptografada, email)
        )
        conexao.commit()

        messagebox.showinfo("Sucesso", "Senha atualizada com sucesso!")

       

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        return False
    
    finally:
        cursor.close()
        conexao.close()
    return True