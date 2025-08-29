import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
import subprocess
import sys

# Load environment variables
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = "recetas_cocina_prueba" # Hardcoded as per user's request

# Configure password hashing context
pwd_context = CryptContext(schemes=["bcrypt", "sha256_crypt"], deprecated="auto")

def get_mysql_command():
    """
    Attempts to find the mysql client executable.
    """
    mysql_cmd = "mysql"
    try:
        subprocess.run([mysql_cmd, "--version"], check=True, capture_output=True)
        return mysql_cmd
    except FileNotFoundError:
        print("Error: 'mysql' command not found in PATH.", file=sys.stderr)
        print("Please ensure MySQL client is installed and its 'bin' directory is in your system's PATH.", file=sys.stderr)
        print("Alternatively, provide the full path to 'mysql.exe' below.", file=sys.stderr)
        
        # Common paths for Windows
        common_paths = [
            "C:\\Program Files\\MySQL\\MySQL Server 8.0\\bin\\mysql.exe",
            "C:\\Program Files\\MySQL\\MySQL Server 5.7\\bin\\mysql.exe",
            "C:\\xampp\\mysql\\bin\\mysql.exe",
            "C:\\wamp\\bin\\mysql\\mysql8.0.0\\bin\\mysql.exe", # Example for WAMP
        ]
        for path in common_paths:
            if os.path.exists(path):
                print(f"Found at common path: {path}", file=sys.stderr)
                return path
        
        sys.exit(1) # Exit if mysql command is not found

def execute_sql_file_with_mysql_client(sql_file_path, db_name=None):
    """
    Executes an SQL file using the mysql command-line client.
    """
    mysql_cmd = get_mysql_command()
    
    command = [mysql_cmd, "-u", DB_USER]
    if DB_PASSWORD:
        command.append(f"-p{DB_PASSWORD}") # -p with no space for password
    
    if db_name:
        command.append(db_name) # Specify database to use

    print(f"Executing SQL file: {sql_file_path}...")
    try:
        with open(sql_file_path, 'r', encoding='utf8') as f:
            process = subprocess.run(command, stdin=f, check=True, capture_output=True, text=True)
            print(process.stdout)
            if process.stderr:
                print(process.stderr, file=sys.stderr)
        print(f"Successfully executed {sql_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing SQL file: {e}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: MySQL client not found at '{mysql_cmd}'. Please check your PATH or provide full path.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

def setup_database():
    """
    Sets up the recetas_cocina_prueba database from scratch.
    """
    print(f"Attempting to connect to MySQL server at {DB_HOST} as {DB_USER}...")
    try:
        # Connect without specifying a database to manage databases
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Drop database if it exists
        print(f"Dropping database {DB_NAME} if it exists...")
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
        
        # Create database
        print(f"Creating database {DB_NAME}...")
        cursor.execute(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Database {DB_NAME} created successfully.")

    except Error as e:
        print(f"Error connecting to MySQL or managing database: {e}", file=sys.stderr)
        sys.exit(1)

    # Execute the SQL schema file
    sql_file_path = os.path.join(os.path.dirname(__file__), "RECETAS-API", "database", "recetas_db.sql")
    execute_sql_file_with_mysql_client(sql_file_path, DB_NAME)

    # Update admin password to a known hash
    print("Updating admin user password...")
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        admin_password_hash = pwd_context.hash("admin123")
        query = "UPDATE usuarios SET password_hash = %s WHERE email = 'admin@recetas.com';"
        cursor.execute(query, (admin_password_hash,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print("Admin user password updated successfully.")
        else:
            print("Admin user not found or password not updated (might not exist yet).")
            
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error updating admin password: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    setup_database()
    print("\nDatabase setup complete. You can now run the Flask server.")
