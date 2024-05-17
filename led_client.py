import socket

def led_cmd(cmd):
    """Sendet den LED-Status über einen Socket"""
    socket_path = "/tmp/led_socket"
    with socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM) as client_socket:
        client_socket.sendto(cmd.encode(), socket_path)

