#!/usr/bin/env python3
"""
Test if frontend can make API requests
"""

import subprocess
import time
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import threading
import socketserver

def test_frontend_request():
    print("🧪 Testing Frontend API Request...")
    
    # Create a simple test page
    test_html = """
<!DOCTYPE html>
<html>
<head>
    <title>API Test</title>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body>
    <h1>API Test Page</h1>
    <button onclick="testAPI()">Test API</button>
    <div id="result"></div>
    
    <script>
        async function testAPI() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = 'Testing...';
            
            try {
                const response = await axios.get('http://localhost:5000/api/courses');
                resultDiv.innerHTML = `
                    <h3>✅ Success!</h3>
                    <p>Status: ${response.status}</p>
                    <p>Courses Found: ${response.data.courses.length}</p>
                    <pre>${JSON.stringify(response.data.courses[0], null, 2)}</pre>
                `;
            } catch (error) {
                resultDiv.innerHTML = `
                    <h3>❌ Error!</h3>
                    <p>Error: ${error.message}</p>
                    <p>Status: ${error.response?.status}</p>
                    <p>Response: ${error.response?.data || 'No response'}</p>
                `;
                console.error('Full error:', error);
            }
        }
        
        // Auto-test on load
        window.onload = () => {
            setTimeout(testAPI, 1000);
        };
    </script>
</body>
</html>
    """
    
    # Write test HTML file
    with open('test_api.html', 'w') as f:
        f.write(test_html)
    
    print("✅ Test page created: test_api.html")
    print("🌐 Open this file in your browser to test the API directly")
    print("📱 Or access: http://localhost:8080/test_api.html")
    
    # Start a simple server
    class TestHandler(SimpleHTTPRequestHandler):
        def end_headers(self):
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", 8080), TestHandler) as httpd:
            print("🚀 Test server running on http://localhost:8080")
            print("📝 Open http://localhost:8080/test_api.html to test API")
            threading.Thread(target=httpd.serve_forever, daemon=True).start()
            
            # Open browser
            time.sleep(1)
            webbrowser.open('http://localhost:8080/test_api.html')
            
            # Keep running for 30 seconds
            time.sleep(30)
            
    except KeyboardInterrupt:
        print("\n🛑 Test stopped")
    except Exception as e:
        print(f"❌ Error starting test server: {e}")

if __name__ == "__main__":
    test_frontend_request()
