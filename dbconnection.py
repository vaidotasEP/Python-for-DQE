import sqlite3
import datetime


class DBConnection:
    """
    Class to implement interaction with sqlite3 database.

    Attributes:
        conn: database connection object
        cur: database curser object

    Methods:
        select(table_name: str): selects all from the given database table
        create_table(table_name: str, data: dict): creates a database table using keys of the passed dictionary as
            names of the table fields
        record_exists(table_name: str, data: dict) -> bool: returns True if a record containing specified data already
            exists in a given database table, returns False otherwise
        insert(table_name: str, data: dict):
            inserts a record contained in a 'data' param to the specified database table
        table_exists(table_name: str) -> bool: returns True if a table with the given name exists within the database,
            returns False otherwise.
        close_db_connection(): cleanup - close database cursor and close the database object

        find_city(table_name: str, city: str): returns records if a given table exists in the database, and it contains
            an entry for a given city
    """

    def __init__(self, database_name: str):
        with sqlite3.connect(database_name) as self.conn:
            self.cur = self.conn.cursor()

    def select(self, table_name: str) -> [tuple]:
        if self.table_exists(table_name):
            print(f"The table '{table_name}' exists.")
            self.cur.execute(f'select * from {table_name};')
            return self.cur.fetchall()
        else:
            print(f"The table '{table_name}' does not exist.")
            return None

    def find_city(self, table_name: str, city: str) -> [tuple]:
        if self.table_exists(table_name):
            # print(f"The table '{table_name}' exists.")
            self.cur.execute(f"SELECT * FROM {table_name} WHERE city='{city}';")
            return self.cur.fetchall()
        else:
            print(f"The table '{table_name}' does not exist.")
            return None

    def create_table(self, table_name: str, data: dict):
        fields_def = ''
        for field in data.keys():
            fields_def += field + ' TEXT NOT NULL, '
        self.cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name}(
                id INTEGER PRIMARY KEY,
                {fields_def} 
                timestamp timestamp NOT NULL
            )
        ''')

    def record_exists(self, table_name: str, data: dict) -> bool:
        fields_def = ''
        for field, value in data.items():
            fields_def += field + f"= '{value}' AND "
        fields_def = fields_def[:-4]

        query = f"SELECT id FROM {table_name} WHERE {fields_def}"
        # print(query)

        self.cur.execute(query)
        data = self.cur.fetchone()
        if data is None:
            # print('There is no such post')
            return False
        else:
            print(f'Post found with id {data[0]}')
            return True

    def insert(self, table_name: str, data: dict):
        if not self.table_exists(table_name):
            print(f"The table '{table_name}' does not exist and will be created.")
            self.create_table(table_name, data)

        if self.record_exists(table_name, data):
            print(f'Such post already exists in the database and will not be added.')
        else:
            fields_def = ''
            values_def = ''
            for field, value in data.items():
                fields_def += field + ', '
                values_def += f"'{value}', "
            fields_def = fields_def[:-2]
            values_def = values_def[:-2]

            query = f"INSERT INTO {table_name} ({fields_def}, timestamp) VALUES ({values_def}, '{datetime.datetime.now()}');"
            # print(query)
            self.cur.execute(query)
            self.conn.commit()

    def table_exists(self, table_name: str):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        self.cur.execute(query)
        return self.cur.fetchone() is not None

    def close_db_connection(self):
        self.cur.close()
        self.conn.close()


if __name__ == "__main__":
    dbcon = DBConnection('newsfeed.db')
    news = {
        'body': 'Hello. This is news body.',
        'city': 'Vilnius'
    }
    dbcon.insert('news', news)

    a = dbcon.select('news')
    print(a)
