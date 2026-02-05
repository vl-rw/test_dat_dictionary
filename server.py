import http.server
import socketserver
import json
import urllib.parse

PORT = 8000

JSON_FILE = "data.json"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        if self.path == '/sentences.json':
            self.path = '/sentences.json'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        message1 = data.get('message1', [''])[0]
        message2 = data.get('message2', [''])[0]
        message3 = data.get('message3', [''])[0]
        message4 = data.get('message4', [''])[0]
        message5 = data.get('message5', [''])[0]
        message6 = data.get('message6', [''])[0]

        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            json_data = {}

        json_data['message1'] = message1
        json_data['message2'] = message2
        json_data['message3'] = message3
        json_data['message4'] = message4
        json_data['message5'] = message5
        json_data['message6'] = message6

        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        # Отвечаем браузеру
        self.send_response(200)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Запускаем сервер
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Server running on port {PORT}")
    print(f"http://localhost:8000/")
    httpd.serve_forever()
