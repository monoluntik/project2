import sqlite3 as db


def create_tables():
    cu = db.connect(database='project2.db') 
    c = cu.cursor()
    c.execute("""create table if not exists curs_balance(
            currency varchar(25) primary key,
            buy decimal,
            sell decimal,
            quantity decimal
        )""")

    c.execute("""create table if not exists history(
            currency varchar(25),
            side varchar(25),
            price decimal,
            quantity decimal,
            total_price decimal,
            wdate date,
            wtime time
        )""")

def connection():
    conn = db.connect('project2.db')
    return conn