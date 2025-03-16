import sys
import socket
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QGridLayout, QLineEdit, QFileDialog

# G-901 Motion Controller Connection Details
HOST = "10.0.0.100"
PORT = 701

def test_connection(output_widget):
    """Check connection to the motion controller."""
    try:
        with socket.create_connection((HOST, PORT), timeout=5):
            output_widget.append(f"Connected to {HOST}:{PORT}")
            return True
    except Exception as e:
        output_widget.append(f"Connection failed: {e}")
        return False

def send_command(command, output_widget):
    """Send a command to the motion controller and display the response."""
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            sock.sendall((command + '\r').encode('ascii'))  # Send command
            response = sock.recv(4096).decode('ascii')  # Read response
            output_widget.append(f"Command Sent: {command}")
            output_widget.append(f"Response: {response}")
            
            # Wait for the movement to complete
            time.sleep(0.5)
            
            # Send ?FPOS command to get current position
            sock.sendall("?FPOS\r".encode('ascii'))
            position_response = sock.recv(4096).decode('ascii')
            output_widget.append(f"Current Position: {position_response}")
    except Exception as e:
        output_widget.append(f"Error: {e}")

def send_gcode_file(file_path, output_widget):
    """Read G-code from a file and send each line to the controller."""
    try:
        with open(file_path, 'r') as file:
            for line in file:
                command = line.strip()
                if command:
                    send_command(command, output_widget)
                    time.sleep(0.2)  # Short delay to avoid command overlap
    except FileNotFoundError:
        output_widget.append(f"Error: File {file_path} not found.")

class MotionControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("G-901 Motion Controller")
        self.setGeometry(100, 100, 500, 500)
        
        layout = QVBoxLayout()
        
        # Output Display
        self.output_display = QTextEdit(self)
        self.output_display.setReadOnly(True)
        layout.addWidget(self.output_display)
        
        # Connection Check
        test_connection(self.output_display)
        
        # Manual Command Input
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter G-code command")
        layout.addWidget(self.command_input)
        
        self.btn_send_command = QPushButton("Send Command")
        self.btn_send_command.clicked.connect(self.send_manual_command)
        layout.addWidget(self.btn_send_command)
        
        # File Selection Button
        self.btn_load_file = QPushButton("Load G-code File")
        self.btn_load_file.clicked.connect(self.load_file)
        layout.addWidget(self.btn_load_file)
        
        # Grid Layout for Movement Buttons
        grid = QGridLayout()
        
        self.btn_y_plus = QPushButton("Move Y+")
        self.btn_y_plus.clicked.connect(lambda: send_command("N10 G01 Y10 F500", self.output_display))
        grid.addWidget(self.btn_y_plus, 0, 1)
        
        self.btn_x_minus = QPushButton("Move X-")
        self.btn_x_minus.clicked.connect(lambda: send_command("N20 G01 X-10 F500", self.output_display))
        grid.addWidget(self.btn_x_minus, 1, 0)
        
        self.btn_home = QPushButton("Home XYZ")
        self.btn_home.clicked.connect(lambda: send_command("N70 G01 X0 Y0 Z0 F200", self.output_display))
        grid.addWidget(self.btn_home, 1, 1)
        
        self.btn_x_plus = QPushButton("Move X+")
        self.btn_x_plus.clicked.connect(lambda: send_command("N30 G01 X10 F500", self.output_display))
        grid.addWidget(self.btn_x_plus, 1, 2)
        
        self.btn_y_minus = QPushButton("Move Y-")
        self.btn_y_minus.clicked.connect(lambda: send_command("N40 G01 Y-10 F500", self.output_display))
        grid.addWidget(self.btn_y_minus, 2, 1)
        
        layout.addLayout(grid)
        
        # Z-Axis Buttons
        self.btn_z_up = QPushButton("Move Z Up")
        self.btn_z_up.clicked.connect(lambda: send_command("N50 G01 Z10 F500", self.output_display))
        layout.addWidget(self.btn_z_up)
        
        self.btn_z_down = QPushButton("Move Z Down")
        self.btn_z_down.clicked.connect(lambda: send_command("N60 G01 Z-10 F500", self.output_display))
        layout.addWidget(self.btn_z_down)
        
        self.setLayout(layout)
    
    def send_manual_command(self):
        command = self.command_input.text().strip()
        if command:
            send_command(command, self.output_display)
            self.command_input.clear()
    
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open G-code File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            send_gcode_file(file_path, self.output_display)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MotionControlGUI()
    window.show()
    sys.exit(app.exec_())