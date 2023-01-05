from email.mime import image
from os import link, name
import psycopg2
from psycopg2._psycopg import connection 
 
class Krysha_parse_sql: 
    def __init__(self, conn: connection) -> None: 
        self.conn = conn 
        self.cursor = conn.cursor() 
    def create_table(self): 
        query = """ 
        CREATE TABLE krysha_parsess ( 
            id SERIAL PRIMARY KEY,
            name VARCHAR(10000) NOT NULL, 
            link VARCHAR(10000) NOT NULL, 
            image VARCHAR(10000) NOT NULL, 
            price VARCHAR(100),
            address VARCHAR(10000),
            autor VARCHAR(1000),
            autor_link VARCHAR(1000));""" 
            
        self.cursor.execute(query=query)
        self.conn.commit()
        print('Table created success')
    def register(self, 
                 name,
                 link,
                 image,
                 price,
                 address,
                 autor):
        query = f"""
        INSERT INTO krysha_parsess (
            name, link, image, price, address, autor)
        VALUES('{name}','{link}', '{image}', {price}, '{address}', '{autor}');"""
        
        self.cursor.execute(query=query) 
        self.conn.commit() 
    
    
import psycopg2
conn = psycopg2.connect( 
    dbname='db_123', 
    user='salikh', 
    password='12345', 
    host='localhost' 
) 


krysha_parse_sql_orm = Krysha_parse_sql(conn=conn)
# krysha_parse_sql_orm.create_table()