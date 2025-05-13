from tkinter import messagebox
from db.conexao import conectar
from auth.login import usuario_logado


def confirmar_todas_saidas(tabela):
    conn = None
    cursor = None
    try:
        todos_itens = tabela.get_children()
        if not todos_itens:
            messagebox.showwarning("Atenção", "Nenhum produto na lista de saídas.")
            return

        nome_usuario = usuario_logado.nome

        conn = conectar()
        cursor = conn.cursor()

        for item in todos_itens:
            dados = tabela.item(item, "values")
            id_produto = dados[0]
            nome_produto = dados[1].strip().upper()
            categoria = dados[2].strip().upper()
            estoque_atual = int(dados[3])
            quantidade = dados[4]
            motivo = dados[5].strip().upper()
            responsavel = nome_usuario.upper()

            if not quantidade or not motivo:
                messagebox.showwarning("Atenção", "Todos os produtos devem ter quantidade e motivo.")
                return

            try:
                quantidade = int(quantidade)
            except ValueError:
                messagebox.showerror("Erro", f"Quantidade inválida no produto '{nome_produto}'.")
                return

            if quantidade > estoque_atual:
                messagebox.showwarning("Atenção", f"Quantidade de saída maior que o estoque para o produto '{nome_produto}'.")
                return

            novo_estoque = estoque_atual - quantidade

            # Atualiza o estoque
            cursor.execute("UPDATE estoque SET estoque = %s WHERE id = %s", (novo_estoque, id_produto))

            # Registra a saída
            cursor.execute("""
                INSERT INTO saidas (nome_produto, categoria, quantidade, motivo, responsavel,data_saida)
                VALUES (%s, %s, %s, %s,%s, CURRENT_DATE)
            """, (nome_produto, categoria, quantidade, motivo,responsavel))

        conn.commit()
        messagebox.showinfo("Sucesso", "Todas as saídas foram registradas com sucesso.")
        for item in todos_itens:
            tabela.delete(item)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao registrar as saídas: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
