import os
import traceback
from functools import reduce

import mysql.connector

class ArkNight:

    def __init__(self, host, port, user_name, password, db_name):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.conn = None

    def connect_to_mysql(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user_name,
                password=self.password,
                database=self.db_name,
            )

        except Exception as e:
            return False, traceback.format_exc()

        return True, ''

    def insert_into_mysql(self, path:str):

        cursor = self.conn.cursor()

        for root, dir_list, file_list in os.walk(path):

            for file_name in file_list:

                if file_name.endswith('.txt'):

                    file_path = os.path.join(root, file_name)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            items = f.readlines()

                        for item in items:
                            if item.startswith('"'):
                                operator_name, line = item.split(':')[0].replace('"',''), item.split(':')[1]

                                query = """INSERT INTO operator_lines (operator_name, line) VALUES (%s, %s)"""

                                tuple_insert = (operator_name, line)

                                cursor.execute(query, tuple_insert)

                    except Exception as e:

                        with open(file_path, 'r', encoding='gbk') as f:
                            items = f.readlines()

                        for item in items:
                            if item.startswith('"'):
                                operator_name, line = item.split(':')[0].replace('"',''), item.split(':')[1]

                                query = """INSERT INTO operator_lines (operator_name, line) VALUES (%s, %s)"""

                                tuple_insert = (operator_name, line)

                                cursor.execute(query, tuple_insert)

        self.conn.commit()

        cursor.close()
        self.conn.close()

if __name__ == '__main__':
    x = [7000 + x * 400 for x in range(0,9)]

    sumup = sum([3 * y for y in x])

    print(sumup / 24)









