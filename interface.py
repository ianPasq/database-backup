import click
import os
from db_manager import DBManager
from manage_backup import BackupManager


@click.group()
def cli():
    pass



@click.command()
@click.option("--db-type", type=click.Choice(["mysql", "postgresql", "mongodb"]), require=True, help="Database type")
@click.option("--host", default="localhost", help="Database host")
@click.option("--user", default=lambda: os.getenv("DB_USER", "root"), help="Database username")
@click.option("--password", default=lambda: os.getenv("DB_PASSWORD", ""), help="Database password")
@click.option("--database", default=lambda: os.getenv("DB_NAME", ""), help="Database name")
@click.option("--port", type=int, default=None, help="Database port")
@click.option("--backup-dir", default="backups", help="Directory to store backups")


def connect(db_type, host, user, password, database, port):
    if not port:
        port = {"mysql": 3306, "postgresql": 5432, "mongodb": 27017}[db_type]

    db = DBManager(db_type, host, user, password, database, port)
    conn = db.connect()

    if conn:
        click.echo(f"Successfully connected to {db_type} at {host}:{port}")
        db.close()
    else:
        click.echo(f"Failed to connect to {db_type}")
    

def backup(db_type, host, user, password, database, port, backup_dir):
    if not port:
        port = { "mysql": 3306, "postgresql": 5432, "mongodb":27017}[db_type]

    manage_backup = BackupManager(db_type, host, user, password, database, port, backup_dir)
    manage_backup.backup()



    # connect to mysql: python cli.py --db-type mysql --user root --password secret --database testdb --host 127.0.0.1

    # connect to postgre: python cli.py --db-type postgresql --user postgres --password secret --database mydb --host 127.0.0.1 

    # connect to mogodb: python cli.py --db-type mongodb --user mongo --password secret --database testdb --host 127.0.0.1



@click.command()
@click.option("--db-type", type=click.Choice(["mysql", "postgresql", "mongodb"]), required=True, help="Database type")
@click.option("--host", default="localhost", help="Database host")
@click.option("--user", default=lambda: os.getenv("DB_USER", "root"), help="Database username")
@click.option("--password", default=lambda: os.getenv("DB_PASSWORD", ""), help="Database password")
@click.option("--database", default=lambda: os.getenv("DB_NAME", ""), help="Database name")
@click.option("--port", type=int, default=None, help="Database port")
@click.argument("query")
@click.argument("backup_file")

def execute(db_type, host, user, password, database, port, query):
    if not port:
        port = {"mysql": 3306, "postgresql": 5432, "mongodb": 27017}[db_type]

    db = DBManager(db_type, host, user, password, database, port)
    conn = db.connect()

    if conn:
        click.echo(f"Executing query on {db_type}...")
        db.execute_query(query)
        db.close()
    else:
        click.echo(f"Failed to connect to {db_type}")

cli.add_command(connect)
cli.add_command(execute)


def restore(db_type, host, user, password, database, port, backup_file):
    if not port:
        port = {"mysql": 3306, "postgresql": 5432, "mongodb": 27017}[db_type]


    manage_backup = BackupManager(db_type, host, user, password, database, port)
    manage_backup.restore(backup_file)

cli.add_command(backup)
cli.add_command(restore)


if __name__ == "__main__":
    cli()


















