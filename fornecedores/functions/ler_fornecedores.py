from tkinter import messagebox
from db.conexao import conectar

def buscar_produtos(tipo_pesquisa, entrada_nome, entrada_cnpj, tabela):
    try:
        conn = conectar()
        cursor = conn.cursor()

        consulta_base = "SELECT id, nome, cnpj, telefone, email, endereco, data_cadastro FROM fornecedores"
        filtros = []
        valores = []

        tipo = tipo_pesquisa.get()

        if tipo == "Tudo":
            pass  # Nenhum filtro aplicado

        elif tipo == "Por nome":
            filtros.append("nome ILIKE %s")
            valores.append(f"%{entrada_nome.get()}%")

        elif tipo == "Por cnpj":
            filtros.append("cnpj = %s")
            valores.append(entrada_cnpj.get())

        if filtros:
            consulta_base += " WHERE " + " AND ".join(filtros)

        consulta_base += " ORDER BY id"

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
