import http.server
import socketserver
import json
import csv
import os
import threading

PORT = 8000
CSV_FILE = 'prepared_data.csv'
TEMP_CSV_FILE = 'temp.csv'
FINAL_CSV_FILE = 'final_prepared_data.csv'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            with open(os.path.join(SCRIPT_DIR, 'index.html'), 'r', encoding='utf-8') as f:
                self.wfile.write(f.read().encode('utf-8'))
        elif self.path == '/api/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            data = []
            
            file_to_load = TEMP_CSV_FILE if os.path.exists(TEMP_CSV_FILE) else CSV_FILE
            
            if os.path.exists(file_to_load):
                with open(file_to_load, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        data.append(row)
            self.wfile.write(json.dumps(data).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/save':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                with open(FINAL_CSV_FILE, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['Link', 'Tytuł', 'Opis', 'Tagi', 'Czas'], quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    for row in data:
                        writer.writerow(row)
                
                if os.path.exists(TEMP_CSV_FILE):
                    os.remove(TEMP_CSV_FILE)
                        
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
        elif self.path == '/api/temp_save':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                with open(TEMP_CSV_FILE, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['Link', 'Tytuł', 'Opis', 'Tagi', 'Czas'], quoting=csv.QUOTE_ALL)
                    writer.writeheader()
                    for row in data:
                        writer.writerow(row)
                        
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok"}).encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
        elif self.path == '/api/shutdown':
            self.send_response(200)
            self.end_headers()
            threading.Thread(target=self.server.shutdown).start()
        else:
            self.send_response(404)
            self.end_headers()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serwer selekcji artykułów wystartował na porcie: {PORT}")
    httpd.serve_forever()
