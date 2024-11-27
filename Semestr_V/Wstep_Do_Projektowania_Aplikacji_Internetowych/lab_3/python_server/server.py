import os
import time
import json
import random
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type

DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')

def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Połączono z bazą danych")
            return conn
        except psycopg2.OperationalError:
            print("Błąd połączenia z bazą danych, ponawianie za 5 sekund...")
            time.sleep(5)

conn = connect_to_db()
cursor = conn.cursor()

def initializeDB():
    cursor.execute("SELECT COUNT(*) FROM users WHERE first_name = %s AND last_name = %s", ('Michal', 'Mucha'))
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (first_name, last_name, role) VALUES (%s, %s, %s)",
            ('Michal', 'Mucha', 'Instructor')
        )
        conn.commit()

initializeDB()

class SimpleRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "OK")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        response_data = []
        for user in users:
            response_data.append({
                'id': user[0],
                'first_name': user[1],
                'last_name': user[2],
                'role': user[3]
            })

        self.wfile.write(json.dumps(response_data).encode())

    def do_POST(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())

        newUser: dict = {
            # 'id': random.randint(1, 1000000),
            'first_name': received_data['first_name'],
            'last_name': received_data['last_name'],
            'role': received_data['role']
        }
        # self.users.append(newUser)

        cursor.execute(
            "INSERT INTO users (first_name, last_name, role) VALUES (%s, %s, %s) RETURNING id",
            (newUser['first_name'], newUser['last_name'], newUser['role'])
        )
        user_id = cursor.fetchone()[0]
        conn.commit()

        newUser['id'] = user_id

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json.dumps(newUser).encode())

    def do_DELETE(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())
        user_id = received_data['id']

        # SimpleRequestHandler.users = [user for user in self.users if user['id'] != user_id]

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # self.wfile.write(json.dumps(self.users).encode())

def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
        ) -> None:
    
    server_address: tuple = ('', port)
    httpd: HTTPServer = server_class(server_address, handler_class)

    print(f"Starting HTTP server on port {port}...")

    httpd.serve_forever()

if __name__ == '__main__':
    run()