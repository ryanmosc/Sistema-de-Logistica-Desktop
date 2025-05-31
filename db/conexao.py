import psycopg2

#Conexão com banco de dados Postgress
def conectar():
    try:
        conexao = psycopg2.connect(
            dbname="sistema_db",
            user="postgres",           
            password="q1w2e3", 
            host="localhost", #192.168.1.72
            port="5432"
        )
        print("[OK] Conexão estabelecida com sucesso!, Ação bem sucedida!")
        return conexao
    except Exception as e:
        print(f"[ERRO] Falha na conexão: {e}")
        return None
