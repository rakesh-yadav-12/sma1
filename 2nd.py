# ============ RMI-style Implementation for Google Colab (Fixed) ============

import socket
import json
import threading
import time
import sys

# ============ Remote Interface ============
class AddInterface:
    def sum(self, n1, n2):
        raise NotImplementedError

# ============ Remote Object Implementation ============
class Add(AddInterface):
    def sum(self, n1, n2):
        return n1 + n2

# ============ Server ============
class AddServer:
    def __init__(self, port=9090):
        self.obj = Add()
        self.server_socket = None
        self.running = False
        self.port = port
    
    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Allow reusing the address
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("", self.port))
            self.server_socket.listen(1)
            self.server_socket.settimeout(1)
            self.running = True
            
            print(f"Server is connected and waiting for the client on port {self.port}...")
            
            while self.running:
                try:
                    client_socket, addr = self.server_socket.accept()
                    self.handle_client(client_socket)
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"Server error: {e}")
                    break
                    
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"Server could not connect: Port {self.port} is already in use")
                print("Try stopping previous server or using a different port")
            else:
                print(f"Server could not connect: {e}")
        except Exception as e:
            print(f"Server could not connect: {e}")
    
    def handle_client(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            request = json.loads(data)
            
            if request["method"] == "sum":
                result = self.obj.sum(request["n1"], request["n2"])
                response = {"result": result}
            
            client_socket.send(json.dumps(response).encode())
            client_socket.close()
        except Exception as e:
            print(f"Error handling client: {e}")
    
    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        print("Server stopped")

# ============ Client ============
class AddClient:
    def __init__(self, port=9090):
        self.port = port
    
    def sum_remote(self, n1, n2):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect(("localhost", self.port))
            
            request = {"method": "sum", "n1": n1, "n2": n2}
            client_socket.send(json.dumps(request).encode())
            
            response = json.loads(client_socket.recv(1024).decode())
            client_socket.close()
            
            return response["result"]
            
        except ConnectionRefusedError:
            print("Client Exception: Connection refused - Server is not running")
            return None
        except socket.timeout:
            print("Client Exception: Connection timeout")
            return None
        except Exception as e:
            print(f"Client Exception: {e}")
            return None

# ============ Main Execution ============

# Try different ports if 9090 is busy
def find_available_port(start_port=9090):
    for port in range(start_port, start_port + 10):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            test_socket.bind(("localhost", port))
            test_socket.close()
            return port
        except OSError:
            continue
    return start_port

print("=" * 50)
print("RMI-style Remote Method Invocation in Colab")
print("=" * 50)

# Find an available port
available_port = find_available_port(9090)
print(f"Using port: {available_port}")

# Stop any existing server threads (if any)
for thread in threading.enumerate():
    if thread.name == "ServerThread":
        print("Stopping existing server...")
        # Can't forcefully stop threads, will use different port

# Start the server in a background thread
server = AddServer(port=available_port)
server_thread = threading.Thread(target=server.start, daemon=True, name="ServerThread")
server_thread.start()

# Wait for server to start
time.sleep(2)

# Create client and make remote calls
client = AddClient(port=available_port)

print("\nMaking remote method calls...")
print("-" * 40)

# Call sum method multiple times
result1 = client.sum_remote(10, 2)
if result1 is not None:
    print(f"The sum of 10 and 2 is: {result1}")

result2 = client.sum_remote(25, 30)
if result2 is not None:
    print(f"The sum of 25 and 30 is: {result2}")

result3 = client.sum_remote(100, 200)
if result3 is not None:
    print(f"The sum of 100 and 200 is: {result3}")

print("-" * 40)
print("\nServer is connected and waiting for the client... (running in background)")
print("Client successfully made remote calls to the server!")
print("\n✨ RMI simulation completed successfully!")
