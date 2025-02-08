import os
import subprocess

class BackupManager:
    def __init__(self, db_type, host, user, password, database, port, backup_dir="backups"):
        self.db_type = db_type.lower()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.backup_dir = backup_dir

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

    def backup(self):
        backup_file = os.path.join(self.backup_dir, f"{self.database}_backup.sql")

        try:

            if self.db_type == "mysql":
                command = f"mysqldump -h {self.host} -P {self.port} -u {self.user} --password={self.password} {self.database} > {backup_file}"
            elif self.db_type == "postgresql":
                os.environ["PGPASSWORD"] = self.password
                command = f"pg_dump -h {self.host} -p {self.port} -U {self.user} -d {self.database} -F c -f {backup_file}"
            elif self.db_type == "mongodb":
                backup_file = os.path.join(self.backup_dir, f"{self.database}_backup")
                command = f"mongodump --host {self.host} --port {self.port} --username {self.user} --password {self.password} --db {self.database} --out {backup_file}"
            else:
                raise ValueError("Unsupported database type for backup.")

            subprocess.run(command, shell=True, check=True)
            print(f"Backup successful: {backup_file}")

        except subprocess.CalledProcessError as e:
            print(f"Error during backup: {e}")

    def restore(self, backup_file):
        try:

            if self.db_type == "mysql":
                command = f"mysql -h {self.host} -P {self.port} -u {self.user} --password={self.password} {self.database} < {backup_file}"
            elif self.db_type == "postgresql":
                os.environ["PGPASSWORD"] = self.password
                command = f"pg_restore -h {self.host} -p {self.port} -U {self.user} -d {self.database} -F c {backup_file}"
            elif self.db_type == "mongodb":
                command = f"mongorestore --host {self.host} --port {self.port} --username {self.user} --password {self.password} --db {self.database} {backup_file}"
            else:
                raise ValueError("Unsupported database type for restore.")

            subprocess.run(command, shell=True, check=True)
            print(f"Restore successful from: {backup_file}")

        except subprocess.CalledProcessError as e:
            print(f"Error during restore: {e}")

