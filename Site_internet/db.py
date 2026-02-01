import psycopg2
import psycopg2.extras

def connect():
  conn = psycopg2.connect(
    dbname = 'dani.laldji_db',
    host = 'sqledu.univ-eiffel.fr',
    password = 'Laldjidani.123',
    cursor_factory = psycopg2.extras.NamedTupleCursor
  )
  conn.autocommit = True
  return conn