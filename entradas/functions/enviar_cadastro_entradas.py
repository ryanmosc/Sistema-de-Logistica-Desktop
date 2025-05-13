from tkinter import messagebox
from db.conexao import conectar

def enviar(entradas):
    try:
        nome = entradas["Nome do Produto"].get().upper().strip()
        categoria = entradas["Categoria"].get()
        fornecedor = entradas["Fornecedor"].get()
        quantidade = int(entradas["Quantidade"].get())
        preco_custo = float(entradas["Preço de Custo"].get())
        preco_venda = float(entradas["Preço de Venda"].get())
        data_entrada = entradas["Data de Entrada"].get_date()
        caminho_arquivo = entradas["Arquivo XML/PDF"].get()

        if not nome:
            messagebox.showerror("Erro", "O campo 'Nome do produto' não pode estar vazio.")
            return
        if quantidade < 0:
            messagebox.showerror("Erro", "O valor de quantidade não pode ser negativo.")
            return

        # Ler conteúdo binário do arquivo
        conteudo_arquivo = None
        nome_arquivo = None
        tipo_arquivo = None
        if caminho_arquivo:
            try:
                with open(caminho_arquivo, "rb") as f:
                    conteudo_arquivo = f.read()
                    nome_arquivo = caminho_arquivo.split("/")[-1]
                    tipo_arquivo = nome_arquivo.split(".")[-1].lower()
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível ler o arquivo: {e}")
                return

        conn = conectar()
        cursor = conn.cursor()

        # Buscar o ID do fornecedor pelo nome
        cursor.execute("SELECT id FROM fornecedores WHERE nome = %s", (fornecedor,))
        fornecedor_result = cursor.fetchone()
        if fornecedor_result is None:
            messagebox.showerror("Erro", "Fornecedor não encontrado.")
            conn.rollback()
            return

        id_fornecedor = fornecedor_result[0]

        # Inserir a entrada e capturar o ID
        cursor.execute("""
            INSERT INTO entradas (
                nome_produto, fornecedor, quantidade, preco_custo,
                preco_venda, data_entrada
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            nome, fornecedor, quantidade, preco_custo,
            preco_venda, data_entrada
        ))
        id_entrada = cursor.fetchone()[0]

        # Inserir o arquivo na tabela 'arquivos' (se existir)
        if conteudo_arquivo and nome_arquivo:
            cursor.execute("""
                INSERT INTO arquivos (
                    id_entrada, nome, tipo, conteudo
                ) VALUES (%s, %s, %s, %s)
            """, (id_entrada, nome_arquivo, tipo_arquivo, conteudo_arquivo))

        # Verifica se o produto já está no estoque
        cursor.execute(
            "SELECT estoque FROM estoque WHERE nome_produto = %s AND id_fornecedor = %s",
            (nome, id_fornecedor)
        )
        resultado = cursor.fetchone()

        if resultado:
            estoque_atual = resultado[0]
            novo_estoque = estoque_atual + quantidade
            cursor.execute("""
                UPDATE estoque
                SET estoque = %s, ultima_atualizacao = CURRENT_TIMESTAMP
                WHERE nome_produto = %s AND id_fornecedor = %s
            """, (novo_estoque, nome, id_fornecedor))
        else:
            cursor.execute("""
                INSERT INTO estoque (
                    nome_produto, estoque, categoria, preco_custo,
                    preco_venda, data_entrada, id_fornecedor
                ) VALUES (%s, %s, %s, %s, %s, CURRENT_DATE, %s)
            """, (nome, quantidade, categoria, preco_custo, preco_venda, id_fornecedor))

        conn.commit()
        messagebox.showinfo("Sucesso", "Entrada cadastrada com sucesso!")

        # Limpar os campos
        for campo in entradas.values():
            if hasattr(campo, "delete"):
                campo.delete(0, "end")
            elif hasattr(campo, "set"):
                campo.set("")

    except ValueError:
        messagebox.showerror("Erro", "Verifique os campos numéricos. Use '.' para decimais.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
