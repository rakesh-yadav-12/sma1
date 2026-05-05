# ============ RMI-style Implementation for Google Colab ============

import socket
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor

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
    def __init__(self):
        self.obj = Add()
        self.server_socket = None
        self.running = False
    
    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(("", 9090))  # Bind to all interfaces in Colab
            self.server_socket.listen(1)
            self.server_socket.settimeout(1)  # 1 second timeout for checking running flag
            self.running = True
            
            print("Server is connected and waiting for the client...")
            
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
                    
        except Exception as e:
            print("Server could not connect:", e)
    
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
    def sum_remote(self, n1, n2):
        try:
            # Create socket and connect to server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect(("localhost", 9090))
            
            # Prepare and send request
            request = {"method": "sum", "n1": n1, "n2": n2}
            client_socket.send(json.dumps(request).encode())
            
            # Receive and parse response
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

# ============ Main Execution in Colab ============

# Method 1: Run server in background thread
print("=" * 50)
print("RMI-style Remote Method Invocation in Colab")
print("=" * 50)

# Start the server in a background thread
server = AddServer()
server_thread = threading.Thread(target=server.start, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(2)

# Create client and make remote calls
client = AddClient()

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

# Optional: Stop the server (uncomment if needed)
# server.stop()
