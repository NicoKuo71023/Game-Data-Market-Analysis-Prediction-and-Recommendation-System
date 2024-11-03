import pymysql
import configparser as cp

import pymysql.cursors


class SqlQuery:

    def __init__(self, config_path="envs/config.ini", database="db_for_da"):
        config_file = cp.ConfigParser()
        config_file.read(config_path)

        self.database = database
        self.connection = pymysql.connect(
            host=config_file["DB"]["host"],
            user=config_file["DB"]["user"],
            password=config_file["DB"]["password"],
            port=int(config_file["DB"]["port"]),
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor,
        )

    def __str__(self):
        return f"SqlQuery - use database: {self.database}"

    @staticmethod
    def _turn_value_to_list(result: dict):
        return [i["Database"] for i in result]

    @property
    def databases(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES;")
            result = cursor.fetchall()
            result = self._turn_value_to_list(result)

        return result

    def sql_search(self, sql):
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

        return result

    def show_table(self):
        if self.database == None:
            raise Exception("SqlQuery obj database is None")

        with self.connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            result = cursor.fetchall()

        return result
