import http.server
import socket
import qrcode
import tkinter as tk
from PIL import Image, ImageTk  # Pillow for handling the QR image
import threading
import time

# Function to get the local IP address
def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))  # Just need a remote address for the socket to connect to
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'  # Fallback to localhost if the network is not available
    finally:
        s.close()
    return ip_address

# Generate the QR code for the URL
def generate_qr_code(url: str):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    # Convert QR code to an image
    img = qr.make_image(fill='black', back_color='white')

    return img

# Function to create the Tkinter window and display the QR code
def create_gui(qr_image):
    root = tk.Tk()
    root.title("QR Code for Local Server")
    
    # Convert the PIL image to something Tkinter can handle
    qr_tk_image = ImageTk.PhotoImage(qr_image)

    # Create a label to display the image
    label = tk.Label(root, image=qr_tk_image)
    label.pack(padx=10, pady=10)

    # Start the Tkinter main loop
    root.mainloop()

# Function to run the HTTP server
def run_http_server(local_ip):
    # Define the server address and port (bind to all network interfaces with '0.0.0.0')
    server_address = ('0.0.0.0', 8080)

    # Create the HTTP server instance
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

    # Print the URL
    print(f"Serving HTTP on http://{local_ip}:8080")

    # Start the HTTP server
    httpd.serve_forever()

# Get the local IP address of the computer
local_ip = get_local_ip()

# Create the URL
url = f"http://{local_ip}:8080"

# Generate the QR code
qr_image = generate_qr_code(url)

# Run the HTTP server in a separate thread
server_thread = threading.Thread(target=run_http_server, args=(local_ip,))
server_thread.daemon = True  # Daemonize to exit when the main program ends
server_thread.start()

# Run the Tkinter GUI in the main thread
create_gui(qr_image)
