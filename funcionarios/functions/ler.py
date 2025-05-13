from tkinter import messagebox
from db.conexao import conectar

def buscar_funcionarios(tipo_pesquisa, entrada_nome, cargo_box, entrada_cpf, tabela):
    try:
        conn = conectar()
        cursor = conn.cursor()

        query_base = """
            SELECT nome, last_name, cargo, cpf, email, telefone, data_admissao, salario 
            FROM funcionarios
        """
        filtros = []
        valores = []

        tipo = tipo_pesquisa.get()
        nome = entrada_nome.get().strip()
        cargo = cargo_box.get().strip()
        cpf = entrada_cpf.get().strip()

        # Aplicando lógica dos filtros
        if tipo == "Por nome" and nome:
            filtros.append("nome ILIKE %s")
            valores.append(f"%{nome}%")

        elif tipo == "Por cargo" and cargo != "NULO":
            filtros.append("cargo = %s")
            valores.append(cargo)

        elif tipo == "CPF" and cpf:
            filtros.append("cpf = %s")
            valores.append(cpf)

        elif tipo == "Tudo":
            if cargo != "NULO":
                filtros.append("cargo = %s")
                valores.append(cargo)

        # Monta consulta SQL final
        if filtros:
            query_base += " WHERE " + " AND ".join(filtros)

        cursor.execute(query_base, tuple(valores))
        resultados = cursor.fetchall()

        # Limpa resultados anteriores da tabela
        for item in tabela.get_children():
            tabela.delete(item)

        # Insere os novos resultados
        for linha in resultados:
            tabela.insert("", "end", values=linha)

        cursor.close()
        conn.close()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar funcionários: {e}")
