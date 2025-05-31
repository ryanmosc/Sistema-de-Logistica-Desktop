# views/home_view.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from metricas.metricas_views.ler_view_metricas import abrir_dashboard  # Correct import
from estoque.views_estoque.ler_view import exibir_tela_pesquisa
from funcionarios.views_funcionarios.ler_view import exibir_tela_funcionarios
from saidas.views_saidas.ler_view_saidas import abrir_tela_saidas
from views.sobre_view import abrir_sobre
from others.estoque_baixo import verificar_estoque_baixo
from others.grafico_home import exibir_grafico_barras
from entradas.entradas_view.ler_entradas_view import exibir_entradas
from fornecedores.fornecedores_view.ler_view_fornecedores import exibir_tela_pesquisa_fornecedores

def criar_tela_inicial():
    from auth.login import usuario_logado

    janela = tk.Tk()
    janela.title("Sistema de Gerenciamento - Home")
    janela.geometry("1100x600")
    janela.resizable(False, False)

    # ==== Imagem de fundo ====
    try:
        imagem_fundo = Image.open("images/imagem_fundo.jpg")
        imagem_fundo = imagem_fundo.resize((1100, 600))
        imagem_fundo = ImageTk.PhotoImage(imagem_fundo)
        label_fundo = tk.Label(janela, image=imagem_fundo)
        label_fundo.place(relwidth=1, relheight=1)
    except FileNotFoundError:
        janela.configure(bg="#ecf0f1")

    # ==== Sidebar ====
    sidebar = tk.Frame(janela, bg="#1e2a44", width=220)
    sidebar.pack(side="left", fill="y")

    titulo_sidebar = tk.Label(
        sidebar, text="☰ Menu Principal", bg="#1e2a44", fg="#ffffff",
        font=("Helvetica", 16, "bold"), pady=20
    )
    titulo_sidebar.pack()

    def voltar_inicio():
        janela.destroy()
        criar_tela_inicial()

    def sair():
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            janela.destroy()

    botoes = {
        "🏛 Início": voltar_inicio,
        "📥 Entradas": lambda: exibir_entradas(janela),
        "📋 Fornecedores": lambda: exibir_tela_pesquisa_fornecedores(janela),
        "📚 Estoque": lambda: exibir_tela_pesquisa(janela),
        "👥 Funcionários": lambda: exibir_tela_funcionarios(janela),
        "📤 Saídas": lambda: abrir_tela_saidas(janela),
        "ℹ Metricas": lambda: abrir_dashboard(),  # Remove janela parameter
        "✔ Verificação": verificar_estoque_baixo,
        "🚪 Sair": sair
    }

    for texto, comando in botoes.items():
        btn = tk.Button(
            sidebar, text=texto, font=("Helvetica", 12),
            fg="white", bg="#34495e", activebackground="#3498db",
            activeforeground="white", relief="flat", padx=15,
            pady=10, anchor="w", command=comando,
            borderwidth=0
        )
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3498db"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495e"))
        btn.pack(fill="x", pady=5, padx=10)

    # ==== Rodapé ====
    rodape = tk.Frame(janela, bg="#dfe6e9", height=30)
    rodape.pack(side="bottom", fill="x")

    def obter_cotacao_dolar():
        try:
            response = requests.get("https://economia.awesomeapi.com.br/json/last/USD-BRL")
            if response.status_code == 200:
                dados = response.json()
                cotacao = dados["USDBRL"]["bid"]
                return f"💵 Dólar: R$ {float(cotacao):.2f}"
            else:
                return "Erro ao obter cotação."
        except Exception:
            return "Erro ao obter cotação."

    nome_usuario = usuario_logado.nome
    cotacao_dolar = obter_cotacao_dolar()

    label_usuario = tk.Label(
        rodape, text=f"👤 Bem-vindo(a), {nome_usuario}",
        font=("Helvetica", 10), bg="#dfe6e9", fg="#2c3e50", anchor="w"
    )
    label_usuario.pack(side="left", padx=10)

    label_cotacao = tk.Label(
        rodape, text=cotacao_dolar,
        font=("Helvetica", 10), bg="#dfe6e9", fg="#2c3e50", anchor="e"
    )
    label_cotacao.pack(side="right", padx=10)

    janela.mainloop()

if __name__ == "__main__":
    criar_tela_inicial()