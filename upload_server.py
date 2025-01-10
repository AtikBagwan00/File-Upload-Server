from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import re

HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 8080       # Port number

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class SimpleFileUploadServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>File Upload</title>
        </head>
        <body>
            <h1>Upload File</h1>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <label for="file">Choose file:</label>
                <input type="file" id="file" name="file"><br><br>
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
        '''
        self.wfile.write(html_content.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        content_type = self.headers['Content-Type']
        boundary = content_type.split("boundary=")[-1].encode()
        body = self.rfile.read(content_length)

        # Extract file data between boundaries
        parts = body.split(boundary)
        for part in parts:
            if b"Content-Disposition" in part and b"filename=" in part:
                headers, file_data = part.split(b"\r\n\r\n", 1)
                filename_match = re.search(b'filename="(.+?)"', headers)
                if filename_match:
                    raw_filename = filename_match.group(1).decode()
                    filename = re.sub(r'[\\/*?\":<>|]', '_', raw_filename)  # Sanitize filename

                    file_data = file_data.rsplit(b"\r\n", 1)[0]  # Remove the trailing boundary line
                    with open(os.path.join(UPLOAD_DIR, filename), 'wb') as f:
                        f.write(file_data)

                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"File uploaded successfully.")
                    return

        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Invalid file upload.")

if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), SimpleFileUploadServer)
    print(f"Server started at http://{HOST}:{PORT}")
    server.serve_forever()
