import pymysql

class MySQLConnector:
    """
    This class, `MySQLConnector`, manages MySQL database connections and provides methods to connect, disconnect, and execute SQL queries.

    1. `__init__`: Initializes database connection settings.
    - Parameters: 
        - `host`: Database server IP address.
        - `user`: Username for login.
        - `password`: Login password.
        - `port`: Port for database connection, default is 3306.

    2. `connectDB`: Establishes a connection to a specified database.
    - Parameter: 
        - `database`: Target database name.
    - Prints a message confirming connection.

    3. `disconnect`: Closes the database connection.
    - Prints a message confirming disconnection.

    4. `execute_query`: Executes a given SQL query and returns the result.
    - Parameter:
        - `query`: SQL query to execute.
    - Returns: Query result.
    - Raises an exception if there’s no active connection.

    Example usage:
    Creates an instance of `MySQLConnector`, connects to `g3_db`, and executes a `SHOW TABLES` query.
    """
    def __init__(self, host, user, password, port=3306):
        """
        初始化資料庫連線設置。
        
        :param host: 資料庫主機 IP 地址
        :param user: 使用者名稱
        :param password: 密碼
        :param port: 資料庫連接埠，預設為 3306
        """
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def connectDB(self, database):
        """
        與指定的資料庫建立連線。

        :param database: 目標資料庫名稱
        """
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        print(f"Connected to {database} on {self.host}:{self.port}")

    def disconnect(self):
        """關閉資料庫連線。"""
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")

    def execute_query(self, query):
        """
        執行 SQL 查詢並返回結果。

        :param query: 要執行的 SQL 查詢
        :return: 查詢結果
        """
        if not self.connection:
            raise Exception("No database connection. Please call `connect()` first.")
        
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        
        return result
    
if __name__ == '__main__':
    sql_test = MySQLConnector('192.168.31.130', 'bigred', 'bigred', 32010)
    sql_test.connectDB('g3_db')
    print(sql_test.execute_query('show tables;'))
