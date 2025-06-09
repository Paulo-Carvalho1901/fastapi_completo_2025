from sqlalchemy import create_engine, text, Column, String, Integer, DateTime
from sqlalchemy import MetaData, Table
import sqlalchemy as sa

metadata = MetaData()

comments = Table(
    'comments',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),  # Use Column e defina primary_key
    Column('name', String(255), nullable=False),  # Use Column
    Column('comments', String(255), nullable=False),  # Corrigido o nome da coluna
    Column('live', String(255), nullable=False),  # Use Column
    Column('created_at', DateTime, nullable=True)  # Use Column
)


# CRIADO A ENGINE DE CONEXÃO
engine = create_engine(
    # "postgresql+psycopg2://postgres:D%40vi0406@localhost:5432/faculdade",
    'sqlite:///database.db'  # Use três barras para caminho relativo
)

metadata.create_all(engine)

# # CRIADO A VARIAVEL DE CONEXÃO CON
# with engine.connect() as con:
#     with con.begin():
#     # COMANDO SQL 
#         sql = text('select * from usuarios')
#         # EXECUTANDO O COMANDO SQL NO BANCO CONECTADO
#         result = con.execute(sql)
