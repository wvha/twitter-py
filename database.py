from psycopg2 import pool

# def connect():
#   return psycopg2.connect(user='postgres', password='1234', database='learning', host='localhost', port='5432')

connection_pool = pool.SimpleConnectionPool(1, 5,
                                            database="learning",
                                            user="postgres",
                                            password="1234",
                                            host="localhost")

class CursorFromConnectionFromPool:
  def __init__(self):
    self.connection = None
    self.cursor = None

  def __enter__(self):
    self.connection = connection_pool.getconn()
    self.cursor = self.connection.cursor()
    return self.cursor

  def __exit__(self, exception_type, exception_value, exception_traceback):
    if exception_value is not None:
      self.connection.rollback()
    else:
      self.cursor.close()
      self.connection.commit()
    connection_pool.putconn(self.connection)

class Database:
