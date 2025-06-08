from sqlalchemy import create_engine, text
import psycopg2  # Importe explicitamente o psycopg2

engine = create_engine(
    "postgresql+psycopg2://postgres:D%40vi0406@localhost:5432/faculdade",
    # 'sqlite://'
    echo=True,
)

con = engine.connect()

sql = text('select * from usuarios')

con.execute(sql)

con.close()
