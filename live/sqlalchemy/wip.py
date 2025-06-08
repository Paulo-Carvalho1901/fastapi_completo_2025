from sqlalchemy import create_engine
import psycopg2  # Importe explicitamente o psycopg2

# try:
engine = create_engine(
    "postgresql+psycopg2://postgres:D%40vi0406@localhost:5432/faculdade",
    # 'sqlite://'
    echo=True,
)
print(engine)
print(engine.dialect)
    # Tente uma conexão de teste para verificar se tudo está funcionando
#     with engine.connect() as connection:
#         print("Conexão bem-sucedida!")
# except ImportError as e:
#     print(f"Erro ao importar psycopg2: {e}")
# except Exception as e:
#     print(f"Erro ao conectar ao banco de dados: {e}")

conn = engine.connect()

# print(conn.connection.dbapi_connection)

conn.close()
