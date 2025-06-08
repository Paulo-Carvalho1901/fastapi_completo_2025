from sqlalchemy import create_engine
import psycopg2  # Importe explicitamente o psycopg2

engine = create_engine(
    "postgresql+psycopg2://postgres:D%40vi0406@localhost:5432/faculdade",
    # 'sqlite://'
    echo=True,
)
print(engine.pool)

conn1 = engine.connect()
conn2 = engine.connect()
conn1.close()
conn2.close()
conn3 = engine.connect()

print(engine.pool.status())


# print(conn.connection.dbapi_connection)

# conn.close()
