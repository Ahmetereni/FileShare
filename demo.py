import http.server
import socket
import qrcode
 
# Function to get the local IP address
def get_local_ip()->str:
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

# Get the local IP address of the computer
local_ip = get_local_ip()

# Define the server address and port (bind to all network interfaces with '0.0.0.0')
server_address = ('0.0.0.0', 8080)

# Create the HTTP server instance
httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)

# Create the URL
url = f"http://{local_ip}:8080"

# Generate the QR code
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(url)
qr.make(fit=True)

# Print QR code in terminal
qr.print_ascii()

# Print the IP address for access from other devices
print(f"Serving HTTP on http://{local_ip}:8080")
httpd.serve_forever()
