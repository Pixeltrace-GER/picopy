import socket

def send_led_status(status):
    """Sendet den LED-Status über einen Socket"""
    socket_path = "/tmp/led_socket"
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(status.encode(), socket_path)

# Beispiel, wie der Client verwendet wird:
if __name__ == "__main__":
    print("Client start")
    status = input()
    send_led_status(status)  # Sende den Status "ein"
    
