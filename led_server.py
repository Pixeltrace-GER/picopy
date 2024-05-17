import socket
import os
from gpiozero import LED
from time import sleep

# Socket-Pfad
socket_path = "/tmp/led_socket"

# GPIO-Pin-Zuordnung für die LEDs
leds = {
    "status_led": LED(17),
    "progress_led": LED(27),
    "error_led": LED(22),
    "src_mounted_led": LED(24),
    "dest_mounted_led": LED(23)
}


# Vorhandene Socket-Datei löschen, falls vorhanden
if os.path.exists(socket_path):
    os.remove(socket_path)

# UNIX-Domain-Socket erstellen
server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
server_socket.bind(socket_path)

print("LED-Server läuft und wartet auf Nachrichten...")


def process_command(data):
    led_name = data[0]
    action = data[1]
    led = leds.get(led_name)

    if led:
        if action == "on":
            led.on()
        elif action == "off":
            led.off()
        elif action == "blink":
            blink_on_time = float(data[2]) if len(data) > 2 else 0.5
            blink_off_time = float(data[3]) if len(data) > 3 else 0.5
            blink_n = int(data[4]) if len(data) > 4 else None
            background = data[5] if len(data) > 5 else True
            led.blink(on_time=blink_on_time, off_time=blink_off_time, n=blink_n, background=background)
    else:
        print(f"Unbekannte LED: {led_name}")



try:
    while True:
        data, _ = server_socket.recvfrom(1024)
        received = data.decode()
        #print(f"Nachricht empfangen: {received}")
        # Hier könntest du den LED-Status basierend auf der empfangenen Nachricht ändern

        data_arr = received.split("/")
        print(data_arr)
        process_command(data_arr)

except KeyboardInterrupt:
    pass
finally:
    #Close Socket server
    server_socket.close()
    os.remove(socket_path)
    print("LED-Server gestoppt und Socket-Datei entfernt.")
    #turn off all LEDs
    for led in leds.values():
        led.off()


