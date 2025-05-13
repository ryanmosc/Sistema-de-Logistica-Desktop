import tkinter as tk
from tkinter import filedialog, messagebox
import psycopg2
import os
from db.conexao import conectar


def salvar_arquivo():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF e XML", "*.pdf *.xml")])
    if not caminho:
        return

    nome = os.path.basename(caminho)
    tipo = "PDF" if nome.lower().endswith(".pdf") else "XML"

    try:
        with open(caminho, "rb") as arq:
            conteudo = arq.read()

        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO arquivos (nome, tipo, conteudo) VALUES (%s, %s, %s)",
                    (nome, tipo, psycopg2.Binary(conteudo)))
        conn.commit()
        cur.close()
        conn.close()

        messagebox.showinfo("Sucesso", f"{tipo} '{nome}' salvo!")
        atualizar_lista()
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao salvar: {e}")


def atualizar_lista():
    lista_arquivos.delete(0, tk.END)
    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, nome, tipo FROM arquivos ORDER BY id DESC")
        for linha in cur.fetchall():
            lista_arquivos.insert(tk.END, f"{linha[0]} - {linha[1]} ({linha[2]})")
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar arquivos: {e}")


def abrir_arquivo():
    selecao = lista_arquivos.curselection()
    if not selecao:
        messagebox.showwarning("Atenção", "Selecione um arquivo!")
        return

    item = lista_arquivos.get(selecao[0])
    id_arquivo = item.split(" - ")[0]

    try:
        conn = conectar()
        cur = conn.cursor()
        cur.execute("SELECT nome, conteudo FROM arquivos WHERE id = %s", (id_arquivo,))
        nome, conteudo = cur.fetchone()
        caminho_temp = os.path.join(os.getcwd(), nome)

        with open(caminho_temp, "wb") as f:
            f.write(conteudo)

        os.startfile(caminho_temp)
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao abrir: {e}")


# -------------- Interface Estilizada --------------
janela = tk.Tk()
janela.title("Gerenciador de Arquivos")
janela.geometry("500x500")
janela.configure(bg="white")

# Fonte padrão elegante
FONTE_TITULO = ("Helvetica Neue", 16, "bold")
FONTE_PADRAO = ("Helvetica", 11)

# Frame centralizado
frame = tk.Frame(janela, bg="white")
frame.pack(expand=True)

# Título
tk.Label(frame, text="📂 Gerenciador de Arquivos PDF/XML", bg="white", fg="black", font=FONTE_TITULO).pack(pady=20)

# Botão: Selecionar e salvar
btn_salvar = tk.Button(frame, text="Selecionar e Salvar Arquivo", command=salvar_arquivo,
                       bg="white", fg="black", font=FONTE_PADRAO, width=30,
                       borderwidth=2, relief="solid", cursor="hand2", highlightthickness=0)
btn_salvar.pack(pady=10)

# Lista de arquivos
lista_arquivos = tk.Listbox(frame, width=50, height=10, font=("Courier", 10), bd=1, relief="solid")
lista_arquivos.pack(pady=10)

# Botão: Abrir arquivo
btn_abrir = tk.Button(frame, text="📥 Abrir Arquivo Selecionado", command=abrir_arquivo,
                      bg="white", fg="black", font=FONTE_PADRAO, width=30,
                      borderwidth=2, relief="solid", cursor="hand2", highlightthickness=0)
btn_abrir.pack(pady=10)

# Hover (efeito ao passar o mouse)
def on_enter(e): e.widget['bg'] = 'black'; e.widget['fg'] = 'white'
def on_leave(e): e.widget['bg'] = 'white'; e.widget['fg'] = 'black'

for btn in (btn_salvar, btn_abrir):
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

# Carrega arquivos ao abrir
atualizar_lista()

janela.mainloop()
