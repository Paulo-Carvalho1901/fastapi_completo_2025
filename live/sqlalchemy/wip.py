from sqlalchemy import create_engine, text
import psycopg2  # Importe explicitamente o psycopg2

# CRIADO A ENGINE DE CONEXÃO
engine = create_engine(
    "postgresql+psycopg2://postgres:D%40vi0406@localhost:5432/faculdade",
    # 'sqlite://'
    echo=True,
)

# CRIADO A VARIAVEL DE CONEXÃO CON
with engine.connect() as con:
    with con.begin():
    # COMANDO SQL 
        sql = text('select * from usuarios')
        # EXECUTANDO O COMANDO SQL NO BANCO CONECTADO
        result = con.execute(sql)
