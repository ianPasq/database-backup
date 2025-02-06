import mysql.connector
import pg8000
import pymongo

class DBManager:
    def __init__(self, db_type, host, user, password, database, port):
        self.db_type = db_type.lower()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = None

    def connect(self):
        try:
            if self.db_type == "mysql":
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port
                )
                return self.conn
            elif self.db_type == "postgresql":
                self.conn = pg8000.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port
                )
                return self.conn
            elif self.db_type == "mongodb":
                uri = f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
                self.conn = pymongo.MongoClient(uri)
                return self.conn[self.database]
            else:
                raise ValueError("Unsupported database type. Use mysql, postgresql, or mongodb.")
        except Exception as e:
            print(f"Error connecting to {self.db_type}: {e}")
            return None


    def execute_query(self, query):
        try:
            if not self.conn:
                print("no active connection")
                return None
            
            if self.db_type in ["mysql", "postgresql"]:
                cursor = self.conn.cursor()
                cursor.execute(query)

                if query.strip().lower().startswith("select"):
                    res = cursor.fetchall()
                    for row in res:
                        print(row)
                else:
                    self.conn.commit()
                    print("query executed successfully")

                cursor.close()

            elif self.db_type == "mongodb":
                collection_name, operation = query.split("", 1)
                collection = self.conn[collection_name]

                if operation.lower().startswith("find"):
                    documents = list(collection.find())
                    for doc in documents:
                        print(doc)
                else:
                    print("unsuported mongodb operation via cli. use python scripts for advanced operations")

        except Exception as e:
            print(f"Error executing query: {e}")


    def close(self):
        if self.conn:
            if self.db_type in ["mysql", "postgresql"]:
                self.conn.close()
            elif self.db_type == "mongodb":
                self.conn.client.close()
            print(f"Closed connection to {self.db_type}")
