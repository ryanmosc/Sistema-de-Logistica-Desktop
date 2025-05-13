from tkinter import messagebox
from db.conexao import conectar

def buscar_produtos(tipo_pesquisa, entrada_nome, categoria_box, preco_min, preco_max, tabela):
    try:
        conn = conectar()
        cursor = conn.cursor()

        consulta_base = "SELECT id,nome_produto, estoque, categoria, preco_custo, preco_venda, data_entrada FROM estoque"
        filtros = []
        valores = []

        tipo = tipo_pesquisa.get()
        categoria = categoria_box.get()

        if tipo == "Tudo":
            if categoria and categoria != "NULO":
                filtros.append("categoria = %s")
                valores.append(categoria)

        elif tipo == "Por nome":
            filtros.append("nome_produto ILIKE %s")
            valores.append(f"%{entrada_nome.get()}%")

        elif tipo == "Por categoria":
            if categoria and categoria != "NULO":
                filtros.append("categoria = %s")
                valores.append(categoria)

        elif tipo == "Faixa de preço":
            if preco_min.get():
                filtros.append("preco_venda >= %s")
                valores.append(float(preco_min.get()))
            if preco_max.get():
                filtros.append("preco_venda <= %s")
                valores.append(float(preco_max.get()))

        elif tipo == "Nome + Categoria":
            filtros.append("nome_produto ILIKE %s")
            valores.append(f"%{entrada_nome.get()}%")
            if categoria and categoria != "NULO":
                filtros.append("categoria = %s")
                valores.append(categoria)

        # Se houver filtros, adiciona WHERE na consulta
        if filtros:
            consulta_base += " WHERE " + " AND ".join(filtros)
        consulta_base += " ORDER BY id "
            

        cursor.execute(consulta_base, tuple(valores))
        resultados = cursor.fetchall()

        # Limpa a tabela antes de inserir novos dados
        for item in tabela.get_children():
            tabela.delete(item)

        for linha in resultados:
            tabela.insert("", "end", values=linha)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro na busca: {e}")