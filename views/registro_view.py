from tkinter import Toplevel, Label, Entry, Button
from auth.registro import registrar_usuario

def tela_registro(janela_pai):
    
    registro_janela = Toplevel(janela_pai)
    registro_janela.title("Cadastro de Usuário")
    registro_janela.geometry("300x400")
    registro_janela.resizable(False, False)

    Label(registro_janela, text="Nome").pack(pady=5)
    nome_entry = Entry(registro_janela)
    nome_entry.pack()

    Label(registro_janela, text="Usuário").pack(pady=5)
    usuario_entry = Entry(registro_janela)
    usuario_entry.pack()

    Label(registro_janela, text="Email").pack(pady=5)
    email_entry = Entry(registro_janela)
    email_entry.pack()

    Label(registro_janela, text="Senha").pack(pady=5)
    senha_entry = Entry(registro_janela, show="*")
    senha_entry.pack()
    
    Label(registro_janela, text="Repetir Senha").pack(pady=5)
    repet_entry = Entry(registro_janela, show="*")
    repet_entry.pack()

    Button(
        registro_janela, 
        text="Cadastrar", 
        command=lambda: registrar_usuario(
            nome_entry.get(),
            usuario_entry.get(),
            senha_entry.get(),
            repet_entry.get(),
            email_entry.get()
        )
    ).pack(pady=10)

   
    Button(
        registro_janela, 
        text="Fechar", 
        command=registro_janela.destroy
    ).pack(pady=5)
