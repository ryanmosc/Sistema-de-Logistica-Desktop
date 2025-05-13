# Importando bibliotecas e funções
import tkinter as tk
from PIL import Image, ImageTk
from auth.login import verificar_login
from views.registro_view import tela_registro  

def exibir_tela_login(janela):
    for widget in janela.winfo_children():
        widget.destroy()

    janela.title("Login")
    janela.configure(bg="white")


    frame = tk.Frame(janela, bg="white")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    # === IMAGEM DE PERFIL ===
    try:
        imagem = Image.open("images/login_image1.png")
        imagem = imagem.resize((100, 100))
        imagem_tk = ImageTk.PhotoImage(imagem)
        imagem_label = tk.Label(frame, image=imagem_tk, bg="white")
        imagem_label.image = imagem_tk  
        imagem_label.pack(pady=(0, 15))
    except Exception as e:
        print("Erro ao carregar imagem de perfil:", e)

    # Campo de usuário
    tk.Label(frame, text="Usuário", bg="white", font=("Arial", 10)).pack(pady=5)
    entrada_usuario = tk.Entry(frame, width=30, font=("Arial", 11))
    entrada_usuario.pack()

    # Campo de senha
    tk.Label(frame, text="Senha", bg="white", font=("Arial", 10)).pack(pady=5)
    entrada_senha = tk.Entry(frame, show="*", width=30, font=("Arial", 11))
    entrada_senha.pack()

    # Botão de login
    tk.Button(frame, text="Entrar", width=20, bg="#4CAF50", fg="white", font=("Arial", 10), command=lambda: verificar_login(
        entrada_usuario.get().strip(),
        entrada_senha.get(),
        janela
    )).pack(pady=15)

    # Botão de cadastro (opcional)
    # tk.Button(frame, text="Cadastre-se", width=20, command=lambda: tela_registro(janela)).pack()

    # Outras opções futuras
    # tk.Button(frame, text="Esqueci minha senha").pack(pady=5)
