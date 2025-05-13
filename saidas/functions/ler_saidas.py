from tkinter import messagebox
from db.conexao import conectar
from datetime import datetime

def buscar_produtos_saidas(tipo_pesquisa, entrada_nome, categoria_box, entrada_responsavel, entrada_data_ini, entrada_data_fim, tabela):
    try:
        conn = conectar()
        cursor = conn.cursor()

        consulta_base = """
            SELECT id, nome_produto, quantidade, motivo, responsavel, data_saida 
            FROM saidas
        """

        filtros = []
        valores = []

        tipo = tipo_pesquisa.get()
        nome = entrada_nome.get().strip().upper()
        motivo = categoria_box.get().strip().upper()
        responsavel = entrada_responsavel.get().strip()
        data_ini = entrada_data_ini.get().strip()
        data_fim = entrada_data_fim.get().strip()

        formato = "%Y-%m-%d"

        def tratar_datas():
            if data_ini and data_fim:
                try:
                    data_inicio = datetime.strptime(data_ini, formato)
                    data_final = datetime.strptime(data_fim, formato)
                    filtros.append("data_saida BETWEEN %s AND %s")
                    valores.extend([data_inicio, data_final])
                except ValueError:
                    messagebox.showerror("Erro", "Formato de data inválido. Use AAAA-MM-DD.")
                    return False

            elif data_ini:
                try:
                    data_inicio = datetime.strptime(data_ini, formato)
                    filtros.append("data_saida >= %s")
                    valores.append(data_inicio)
                except ValueError:
                    messagebox.showerror("Erro", "Formato de data inválido. Use AAAA-MM-DD.")
                    return False

            elif data_fim:
                try:
                    data_final = datetime.strptime(data_fim, formato)
                    filtros.append("data_saida <= %s")
                    valores.append(data_final)
                except ValueError:
                    messagebox.showerror("Erro", "Formato de data inválido. Use AAAA-MM-DD.")
                    return False

            return True

        # ===== Tipos de pesquisa =====
        if tipo == "Tudo":
            if motivo != "NULO":
                filtros.append("motivo = %s")
                valores.append(motivo)

        elif tipo == "Por nome":
            if nome:
                filtros.append("nome_produto ILIKE %s")
                valores.append(f"%{nome}%")

        elif tipo == "Por categoria":
            if motivo != "NULO":
                filtros.append("motivo = %s")
                valores.append(motivo)

        elif tipo == "Por responsável":
            if responsavel:
                filtros.append("responsavel ILIKE %s")
                valores.append(f"%{responsavel}%")

        elif tipo == "Nome + Categoria":
            if nome:
                filtros.append("nome_produto ILIKE %s")
                valores.append(f"%{nome}%")
            if motivo != "NULO":
                filtros.append("motivo = %s")
                valores.append(motivo)

        elif tipo == "Por data":
            if not tratar_datas():
                return

        elif tipo == "Por data e categoria":
            if not tratar_datas():
                return
            if motivo != "NULO":
                filtros.append("motivo = %s")
                valores.append(motivo)

        elif tipo == "Por data e nome":
            if not tratar_datas():
                return
            if nome:
                filtros.append("nome_produto ILIKE %s")
                valores.append(f"%{nome}%")

        elif tipo == "Por data e responsável":
            if not tratar_datas():
                return
            if responsavel:
                filtros.append("responsavel ILIKE %s")
                valores.append(f"%{responsavel}%")

        elif tipo == "Por data, nome e categoria":
            if not tratar_datas():
                return
            if nome:
                filtros.append("nome_produto ILIKE %s")
                valores.append(f"%{nome}%")
            if motivo != "NULO":
                filtros.append("motivo = %s")
                valores.append(motivo)

        # Query final
        if filtros:
            consulta_base += " WHERE " + " AND ".join(filtros)

        consulta_base += " ORDER BY data_saida DESC"

        cursor.execute(consulta_base, tuple(valores))
        resultados = cursor.fetchall()

        # Limpa tabela
        for item in tabela.get_children():
            tabela.delete(item)

        # Preenche nova tabela
        for linha in resultados:
            tabela.insert("", "end", values=linha)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro na busca de saídas: {e}")
