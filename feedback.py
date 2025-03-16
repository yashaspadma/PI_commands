import socket

HOST = "10.0.0.100"  # G-901 Controller IP
PORT = 701  # Default ACS Motion Control Ethernet port

def send_command(command, output_widget=None):
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            sock.sendall((command + '\r').encode('ascii'))  # Send command
            
            # Read full response in chunks
            response = b""
            while True:
                chunk = sock.recv(4096)  # Read 4KB at a time
                if not chunk:
                    break
                response += chunk  # Append to response
            
            decoded_response = response.decode('ascii')
            print(f"Command Sent: {command}")  # Show command in console
            print(f"Response: {decoded_response}")  # Show response in console
            
            if output_widget:
                output_widget.append(f"Command Sent: {command}")
                output_widget.append(f"Response: {decoded_response}")
            
            # After movement commands, request position feedback
            if "G01" in command or "G02" in command or "G03" in command:
                send_command("#TPOS", output_widget)
    except Exception as e:
        print(f"Error: {e}")
        if output_widget:
            output_widget.append(f"Error: {e}")

# Test system information command
#send_command("ENABLE(Z)")  # Enable Z-axis
send_command("N1 G01 X20 Y20 Z20 F500")  # Move Z-axis

# Periodic status update
from PyQt5.QtCore import QTimer

def update_status(output_widget):
    send_command("#TPOS", output_widget)  # Get current position
    send_command("#MST", output_widget)  # Get motion status

def start_status_updates(output_widget):
    timer = QTimer()
    timer.timeout.connect(lambda: update_status(output_widget))
    timer.start(5000)  # Update every 5 seconds
    return timer