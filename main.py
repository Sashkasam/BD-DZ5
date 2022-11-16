import psycopg2
def delete_db(conn):
    with conn.cursor() as cur:
        cur.execute("""DROP TABLE phones, clients;
        
        """)


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS clients(
                            id SERIAL PRIMARY KEY,
                            first_name VARCHAR(40) NOT NULL,
                            last_name VARCHAR(40)NOT NULL,
                            email VARCHAR(40)
        );
        
        
        """)

        cur.execute("""CREATE TABLE IF NOT EXISTS phones(
                            id SERIAL PRIMARY KEY,
                            phone_number VARCHAR(20),
                            client_id INTEGER REFERENCES clients(id)
        );
        
        """)

def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO clients (first_name, last_name, email) VALUES(%s, %s, %s);
        
        """,(first_name, last_name,email))


def all_clients(conn):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM clients;
            """)
        print(cur.fetchall())
        cur.execute("""
            SELECT * FROM phones;
            """)
        print(cur.fetchall())


def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO phones (client_id, phone_number) VALUES(%s, %s);
        
        """,(client_id,phone_number))

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""UPDATE clients SET first_name = %s WHERE id = %s;

            """,(first_name, client_id))
        if last_name is not None:
            cur.execute("""UPDATE clients SET last_name = %s WHERE id = %s;

            """,(last_name,client_id))
        if email is not None:
            cur.execute("""UPDATE clients SET email = %s WHERE id = %s;

            """,(email,client_id))
        if phone_number is not None:
            cur.execute("""UPDATE phones SET phone_number = %s WHERE id = %s;

            """,(phone_number,client_id))

def delete_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phones WHERE client_id = %s and phone_number = %s;
        
        
        """,(client_id,phone_number))
    
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM phones WHERE client_id = %s;
        """,(client_id))

        cur.execute("""DELETE FROM clients WHERE id = %s;
        """,(client_id))
        
def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    with conn.cursor() as cur:
        if phone_number is not None:
           cur.execute("""SELECT first_name, last_name, email, phone_number
                            FROM clients c
                            JOIN phones AS p ON c.id = p.client_id
                            WHERE phone_number = %s;
            """,(phone_number,))
        else:
            cur.execute("""SELECT first_name, last_name, email, phone_number
                            FROM clients c
                            JOIN phones AS p ON c.id = p.client_id
                            WHERE first_name = %s or last_name = %s or email = %s;
            """,(first_name, last_name, email))
        print(cur.fetchall())
 


with psycopg2.connect(database="bd_dz5", user="postgres", password="postgres") as conn:
    delete_db(conn)
    create_db(conn)
    add_client(conn, 'Maria', 'Popova', 'popova@gmail.com')
    add_client(conn, 'Ivan', 'Ivanov', 'ivanov@gmail.com')
    add_client(conn, 'Ksenia', 'Petrova', 'petrova@gmail.com')
    add_client(conn, 'Alex', 'Melnikov', 'melnikov@gmail.com')
    add_client(conn, 'Anna', 'Smexova', 'smexova@gmail.com')
    add_phone(conn, 1 , '89121111111')
    add_phone(conn, 2, '89122222222')
    add_phone(conn, 3, '89123333333')
    add_phone(conn, 4, '89124444444')
    add_phone(conn, 5, '89125555555')
    add_phone(conn, 5, '89127777777')
    all_clients(conn)
    change_client(conn, 5, 'Polina')
    change_client(conn, 4, None, 'Samoilov')
    change_client(conn, 1, None, None, 'popova2022@gmail.com')
    change_client(conn, 5, None, None, None, '89126666666')
    delete_phone(conn, 5, '89127777777')
    delete_client(conn, '5')
    find_client(conn, 'Maria')
    find_client(conn, None, 'Ivanov')
    find_client(conn, None, None, 'melnikov@gmail.com')
    find_client(conn, None, None, None, '89127777777')

conn.close()