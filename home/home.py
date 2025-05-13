import tkinter as tk

# Você pode importar as funções do CRUD aqui, tipo:
# from estoque.functions.cadastrar import cadastrar_produto

def abrir_tela_estoque(janela_pai):
    from views.home_view import criar_tela_inicial
    from estoque.views_estoque.cadastrar_view import exibir_formulario_cadastro
    from estoque.views_estoque.ler_view import exibir_tela_pesquisa
    janela_pai.destroy()
    janela_estoque = tk.Tk()
    janela_estoque.title("Estoque")
    janela_estoque.geometry("900x600")
    janela_estoque.configure(bg="#f5f5f5")

    # Topbar
    topbar = tk.Frame(janela_estoque, bg="#2c3e50", height=50)
    topbar.pack(side="top", fill="x")

    botoes = {
        "Cadastrar": lambda: exibir_formulario_cadastro(janela_estoque),
        "Pesquisa": lambda: exibir_tela_pesquisa(janela_estoque),
        "Atualizar": lambda: print("Função atualizar chamada"),
        "Deletar": lambda: print("Função deletar chamada"),
        "Voltar": lambda: (janela_estoque.destroy(), criar_tela_inicial())
    }

    for texto, comando in botoes.items():
        btn = tk.Button(
            topbar,
            text=texto,
            fg="white",
            bg="#34495e",
            activebackground="#1abc9c",
            relief="flat",
            font=("Arial", 12),
            padx=15,
            pady=10,
            command=comando
        )
        btn.pack(side="left", padx=5, pady=5)

    # Área principal
    area_principal = tk.Frame(janela_estoque, bg="#ecf0f1")
    area_principal.pack(expand=True, fill="both")

    label_mensagem = tk.Label(
        area_principal,
        text="📦 Bem-vindo ao módulo de Estoque!",
        font=("Arial", 20),
        bg="#ecf0f1",
        fg="#2c3e50"
    )
    label_mensagem.pack(expand=True)

    janela_estoque.mainloop()

    
def abrir_tela_funcionarios(janela_pai):
    janela_pai.destroy()
    janela_funcionarios = tk.Tk()

    janela_funcionarios.title("Funcionarios")
    janela_funcionarios.geometry("900x600")
    janela_funcionarios.configure(bg="#ecf0f1")

    titulo = tk.Label(
        janela_funcionarios,
        
    )
    titulo.pack(pady=20)
    
def abrir_tela_saidas(janela_pai):
    janela_pai.destroy()
    janela_saidas = tk.Tk()

    janela_saidas.title("Saidas de estoque")
    janela_saidas.geometry("900x600")
    janela_saidas.configure(bg="#ecf0f1")

    titulo = tk.Label(
        janela_saidas,
        
    )
    titulo.pack(pady=20)
    
def abrir_tela_metricas(janela_pai):
    janela_pai.destroy()
    janela_metricas = tk.Tk()

    janela_metricas.title("Metricas e resultados")
    janela_metricas.geometry("900x600")
    janela_metricas.configure(bg="#ecf0f1")

    titulo = tk.Label(
        janela_metricas,
        
    )
    titulo.pack(pady=20)

    
