import click
import os
from db_manager import DBManager

@click.command()
@click.option("--db-type", type=click.Choice(["mysql", "postgresql", "mongodb"]), require=True, help="Database type")
@click.option("--host", default="localhost", help="Database host")
@click.option("--user", default=lambda: os.getenv("DB_USER", "root"), help="Database username")
@click.option("--password", default=lambda: os.getenv("DB_PASSWORD", ""), help="Database password")
@click.option("--database", default=lambda: os.getenv("DB_NAME", ""), help="Database name")
@click.option("--port", type=int, default=None, help="Database port")


def connect(db_type, host, user, password, database. port):
    if not port:
        port = {"mysql": 3306, "postgresql": 5432, "mongodb": 27017}[db_type]

    db = DBManager(db_type, host, user, password, database, port)
    conn = db.connect()

    if conn:
        click.echo(f"Successfully connected to {db_type} at {host}:{port}")
        db.close()
    else:
        click.echo(f"Failed to connect to {db_type}")
    

if __name__ == "__main__":
    connect()


    # connect to mysql: python cli.py --db-type mysql --user root --password secret --database testdb --host 127.0.0.1

    # connect to postgre: python cli.py --db-type postgresql --user postgres --password secret --database mydb --host 127.0.0.1 

    # connect to mogodb: python cli.py --db-type mongodb --user mongo --password secret --database testdb --host 127.0.0.1

