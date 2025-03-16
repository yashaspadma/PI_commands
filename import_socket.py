import socket

HOST = "10.0.0.100"  # Replace with actual G-901 IP
PORT = 701  # ACS Motion Control Ethernet port

def test_connection():
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            print(f"Connected to {HOST}:{PORT}")
    except Exception as e:
        print(f"Connection failed: {e}")

test_connection()
