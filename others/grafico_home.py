def exibir_grafico_barras(frame_pai):
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.pyplot as plt
    from db.conexao import conectar
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nome_produto, SUM(quantidade) AS total_vendido
        FROM saidas
        GROUP BY nome_produto
        ORDER BY total_vendido DESC
        LIMIT 5
    ''')
    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    nomes = [linha[0] for linha in resultado]
    quantidades = [linha[1] for linha in resultado]

    # Criando o gráfico
    fig, ax = plt.subplots(figsize=(7, 5))

    # Tornar o fundo do gráfico transparente
    fig.patch.set_visible('#ffffff')

    bars = ax.bar(nomes, quantidades, color='#1abc9c', edgecolor='none')

    # Estilo do gráfico
    ax.set_title('Top 5 Produtos Mais Vendidos', fontsize=14, fontweight='bold')
    ax.set_xlabel('', fontsize=12)
    ax.set_ylabel(' ', fontsize=12)
    ax.tick_params(axis='x', labelrotation=20, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)

    # Remover bordas pretas
    for spine in ax.spines.values():
        spine.set_visible('#ffffff')

    # Adicionar valores acima das barras
    for bar in bars:
        altura = bar.get_height()
        ax.annotate(f'{int(altura)}',
                    xy=(bar.get_x() + bar.get_width() / 2, altura),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center',
                    fontsize=10,
                    color='black')

    fig.tight_layout()  # Impede corte de rótulos
    canvas = FigureCanvasTkAgg(fig, master=frame_pai)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)
