import socket

HOST = "10.0.0.100"  # G-901 Controller IP
PORT = 701  # Default ACS Motion Control Ethernet port

def send_command(command):
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock: #network connection 
            sock.sendall((command + '\r').encode('ascii')) 
            response = sock.recv(1024).decode('ascii') #formatting
            print(f"Response: {response}")  
    except Exception as e:
        print(f"Error: {e}")  

# Test system information command
#send_command("ENABLE(Z)") # commands
#send_command("ENABLE(X,Y)") # commands
send_command("\rN1 G01 X50 Y50 Z20 F500") # commands
#send_command("N1 G04 P1 ") # commands
#send_command("\rN1 G01 X00 Y0 Z0 F500") # commands
#send_command("#")  # Empty command to trigger execution
#send_command("?FPOS") # commands
#send_command("?FPOS") # commands

