from tkinter import Toplevel, Label, Entry, Button
from auth.recuperar_senha import recuperar_senha


def tela_recuperar_senha(janela_pai):
    
    recuperar_janela = Toplevel(janela_pai)
    recuperar_janela.title("Recuperação de Senha")
    recuperar_janela.geometry("300x400")
    recuperar_janela.resizable(False, False)

    Label(recuperar_janela, text="Email").pack(pady=5)
    email_entry = Entry(recuperar_janela)
    email_entry.pack()



    Label(recuperar_janela, text="Senha").pack(pady=5)
    nova_senha_entry = Entry(recuperar_janela, show="*")
    nova_senha_entry.pack()
    
    Label(recuperar_janela, text="Repetir Senha").pack(pady=5)
    repet_nova_senha_entry = Entry(recuperar_janela, show="*")
    repet_nova_senha_entry.pack()

    Button(
        recuperar_janela, 
        text="Cadastrar", 
        command=lambda: recuperar_senha(
            email_entry.get(),
            nova_senha_entry.get(),
            repet_nova_senha_entry.get(),
            
        )
    ).pack(pady=10)

   
    Button(
        recuperar_janela, 
        text="Fechar", 
        command=recuperar_janela.destroy
    ).pack(pady=5)
