from tkinter import messagebox
from db.conexao import conectar

def buscar_produtos(tipo_pesquisa, entrada_nome, categoria_box,
                    entrada_data_inicial, entrada_data_final,
                    entrada_nome_fornecedor, tabela):
    try:
        conn = conectar()
        cursor = conn.cursor()

        consulta = """
            SELECT id, nome_produto, fornecedor, quantidade, preco_custo, preco_venda, data_entrada,arquivo_xml_pdf,nome_arquivo
            FROM entradas
        """
        filtros = []
        valores = []

        tipo = tipo_pesquisa.get()
        nome = entrada_nome.get().strip()
        categoria = categoria_box.get()
        fornecedor = entrada_nome_fornecedor.get()
        data_inicial = entrada_data_inicial.get_date()
        data_final = entrada_data_final.get_date()

        if tipo == "Tudo":
            if categoria != "NULO":
                filtros.append("categoria = %s")
                valores.append(categoria)

        elif tipo == "Por nome":
            filtros.append("nome_produto ILIKE %s")
            valores.append(f"%{nome}%")

        elif tipo == "Por categoria":
            if categoria != "NULO":
                filtros.append("categoria = %s")
                valores.append(categoria)

        elif tipo == "Por fornecedor":
            if fornecedor != "NULO":
                filtros.append("fornecedor = %s")
                valores.append(fornecedor)

        elif tipo == "Nome + Categoria":
            filtros.append("nome_produto ILIKE %s")
            valores.append(f"%{nome}%")
            if categoria != "NULO":
                filtros.append("categoria = %s")
                valores.append(categoria)

        elif tipo == "Por data":
            filtros.append("data_entrada BETWEEN %s AND %s")
            valores.extend([data_inicial, data_final])

        elif tipo == "Por data e categoria":
            filtros.append("data_entrada BETWEEN %s AND %s")
            valores.extend([data_inicial, data_final])
            if categoria != "NULO":
                filtros.append("categoria = %s")
                valores.append(categoria)

        elif tipo == "Por data e nome":
            filtros.append("data_entrada BETWEEN %s AND %s")
            valores.extend([data_inicial, data_final])
            filtros.append("nome_produto ILIKE %s")
            valores.append(f"%{nome}%")

        elif tipo == "Por data e responsável":
            filtros.append("data_entrada BETWEEN %s AND %s")
            valores.extend([data_inicial, data_final])
            if fornecedor != "NULO":
                filtros.append("fornecedor = %s")
                valores.append(fornecedor)

        elif tipo == "Por data, nome e categoria":
            filtros.append("data_entrada BETWEEN %s AND %s")
            valores.extend([data_inicial, data_final])
            filtros.append("nome_produto ILIKE %s")
            valores.append(f"%{nome}%")
            if categoria != "NULO":
                filtros.append("categoria = %s")
                valores.append(categoria)

        if filtros:
            consulta += " WHERE " + " AND ".join(filtros)

        consulta += " ORDER BY id DESC"

        cursor.execute(consulta, tuple(valores))
        resultados = cursor.fetchall()

        # Limpa a tabela
        for item in tabela.get_children():
            tabela.delete(item)

        for linha in resultados:
            tabela.insert("", "end", values=linha)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao buscar os produtos:\n{e}")
