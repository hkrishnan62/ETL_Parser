#!/usr/bin/env python3
"""
ETL Parser Desktop Application
A desktop wrapper for the ETL Parser web application using PyWebView.
"""

import webview
import threading
import time
import sys
import os
from app import app
import socket

def find_free_port():
    """Find a free port to run the Flask server on."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def start_flask_server(port):
    """Start the Flask server in a separate thread."""
    app.config['SERVER_NAME'] = None  # Allow any host
    app.run(host='127.0.0.1', port=port, debug=False, use_reloader=False)

def main():
    """Main entry point for the desktop application."""
    # Find a free port
    port = find_free_port()
    
    # Start Flask server in a background thread
    flask_thread = threading.Thread(target=start_flask_server, args=(port,), daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    time.sleep(2)
    
    # Create the webview window
    url = f'http://127.0.0.1:{port}'
    
    # Window configuration
    window = webview.create_window(
        title='ETL Parser - SQL Mapping Converter',
        url=url,
        width=1400,
        height=900,
        resizable=True,
        fullscreen=False,
        min_size=(1000, 700),
        background_color='#1a1a1a',
        text_select=True
    )
    
    # Start the GUI
    webview.start(debug=False)

if __name__ == '__main__':
    main()
