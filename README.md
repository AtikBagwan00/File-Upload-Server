# File-Upload-Server

Simple File Upload Server

This repository contains a simple file upload server written in Python using the built-in http.server module. The server allows you to upload files via a basic web interface without the need for external frameworks like Flask.

Features

Minimal dependencies (no external libraries required).

Supports file uploads via HTTP POST.

Automatic creation of an uploads directory if it does not exist.

Secure filename handling to prevent directory traversal attacks.

Usage

Prerequisites

Python 3 installed on your machine.

Running the Server

Clone the repository to your local machine:

git clone https://github.com/yourusername/simple-file-upload-server.git
cd simple-file-upload-server

Run the server:

python3 upload_server.py

Open your browser and navigate to:

http://0.0.0.0:8080

Use the web interface to upload files.

