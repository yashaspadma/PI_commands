import socket
import time

HOST = "10.0.0.100"  # G-901 Controller IP
PORT = 701  # Default ACS Motion Control Ethernet port

def send_command(command):
    """Send a single G-code command to the motion controller."""
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            sock.sendall((command + '\r').encode('ascii'))
            response = sock.recv(4096).decode('ascii')
            print(f"Command Sent: {command}")
            print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")

def send_gcode_file(file_path):
    """Read G-code from a file and send each line to the controller."""
    try:
        with open(r"C:\Users\yyash\Documents\FRACKTAL_WORKS\PI_commands\command.txt", 'r') as file:
            for line in file:
                command = line.strip()  # Remove spaces and newlines
                if command:  # Ignore empty lines
                    send_command(command)
                #send_command("N20")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")

# Send G-code file
send_gcode_file("commands.txt")
