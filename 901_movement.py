import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QGridLayout, QLineEdit

# G-901 Motion Controller Connection Details
HOST = "10.0.0.100"
PORT = 701

def send_command(command, output_widget):
    try:
        with socket.create_connection((HOST, PORT), timeout=5) as sock:
            sock.sendall((command + '\r').encode('ascii'))  # Send command
            response = sock.recv(1024).decode('ascii')  # Receive response
            output_widget.append(f"Response: {response}")  # Display response in GUI
    except Exception as e:
        output_widget.append(f"Error: {e}")

class MotionControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("G-901 Motion Controller")
        self.setGeometry(100, 100, 400, 400)
        
        layout = QVBoxLayout()
        
        # Output Display
        self.output_display = QTextEdit(self)
        self.output_display.setReadOnly(True)
        layout.addWidget(self.output_display)
        
        # Manual Command Input
        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("Enter G-code command")
        layout.addWidget(self.command_input)
        
        self.btn_send_command = QPushButton("Send Command")
        self.btn_send_command.clicked.connect(self.send_manual_command)
        layout.addWidget(self.btn_send_command)
        
        # Grid Layout for Movement Buttons
        grid = QGridLayout()
        
        self.btn_y_plus = QPushButton("Move Y+")
        self.btn_y_plus.clicked.connect(lambda: send_command("N10 G01 Y10 F500", self.output_display))
        grid.addWidget(self.btn_y_plus, 0, 1)
        
        self.btn_x_minus = QPushButton("Move X-")
        self.btn_x_minus.clicked.connect(lambda: send_command("N20 G01 X-10 F500", self.output_display))
        grid.addWidget(self.btn_x_minus, 1, 0)
        
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
        
        # Home Button
        self.btn_home = QPushButton("Home XYZ")
        self.btn_home.clicked.connect(lambda: send_command("N70 G01 X0 Y0 Z0", self.output_display))
        layout.addWidget(self.btn_home)
        
        self.setLayout(layout)
    
    def send_manual_command(self):
        command = self.command_input.text().strip()
        if command:
            send_command(command, self.output_display)
            self.command_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MotionControlGUI()
    window.show()
    sys.exit(app.exec_())