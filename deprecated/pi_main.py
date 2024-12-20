from Class.screen.minihat import Minihat
from Class.camera import camera
import socket
import time

screen = Minihat()
plant_classifier = camera.PlantClassifier()

HOST = '0.0.0.0'
PORT = 65432
# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Allow up to 5 connections
print(f"Server listening on {HOST}:{PORT}")
clients = []

temperature = 0
humidity = 0
light_level = 0

# plant type
# results = plant_classifier.detect_and_classify()
results = "golden"
if results:
    print("Detections:", results)

try:
    while True:
        conn, addr = server_socket.accept()  # Accept a new client
        print(f"Connected by {addr}")
        clients.append(conn)

        while True:
            # Receive data from the client
            data = conn.recv(1024).decode('utf-8')
            if not data:
                print(f"Client {addr} disconnected")
                clients.remove(conn)
                conn.close()
                break

            print(f"Received: {data} from {addr}")

            # Parse the received data
            # Split into two parts: sensor type and value
            parts = data.split(" ", 1)
            if len(parts) == 2:
                sensor_type, value = parts
                try:
                    value = float(value)  # Convert the value to a float
                except ValueError:
                    conn.sendall(b"Invalid value\n")
                    continue

                #  Get the plant type
                plant_type = results

                # Respond based on the sensor type
                if sensor_type == "temp":
                    temperature = value
                    response = f"Temperature received: {value}°C"
                elif sensor_type == "light":
                    light_level = value
                    response = f"Light level received: {value} lux"
                elif sensor_type == "moisture":
                    humidity = value
                    response = f"Moisture level received: {value}%"
                else:
                    response = "Invalid sensor type"
            else:
                response = "Invalid command format. Expected format: <sensor_type> <value>"

            # Send the response back to the client
            conn.sendall(response.encode('utf-8'))

            # Plant care instruction logic
            """
                Golden:
                    temperature: 15-29 °C
                    humidity: 50-60 %
                    light: 5000-15000 lux

                Ribbon:
                    temperature: 21-32 °C
                    humdity: 40-60%
                    light: 10000-20000 lux
            """
            tmpmsg = "No warnings"
            hmdmsg = "No warnings"
            ligmsg = "No warnings"
            if plant_type == "golden":
                print("gggg")
                if temperature < 15:
                    tmpmsg = 'Environmeent temperature too low'
                elif temperature > 29:
                    tmpmsg = 'Environmeent temperature too high'
                if humidity < 50.00:
                    hmdmsg = 'Low environmental humidity'
                    print("low water")
                    conn.sendall(hmdmsg.encode('utf-8'))
                elif humidity > 60.00:
                    hmdmsg = 'High environmental humidity'
                if light_level < 5000:
                    ligmsg = 'Excessive environmental light'
                elif light_level > 15000:
                    ligmsg = 'Low environmental light'

            elif plant_type == "ribbon":
                if temperature < 21:
                    tmpmsg = 'Environmeent temperature too low'
                if temperature > 29:
                    tmpmsg = 'Environmeent temperature too high'
                if humidity < 0.4:
                    hmdmsg = 'Low environmental humidity'
                    conn.sendall(hmdmsg.encode('utf-8'))
                if humidity > 0.6:
                    hmdmsg = 'High environmental humidity'
                if light_level < 10000:
                    ligmsg = 'Excessive environmental light'
                if light_level > 20000:
                    ligmsg = 'Low environmental light'


            # Button controls (implement functionality as needed)
            if screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_A):
                screen.display_BUTTON_A(temperature, humidity, light_level, 1)
            elif screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_B):
                screen.display_BUTTON_B(tmpmsg, hmdmsg, ligmsg)
            elif screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_X):
                pass
            elif screen.displayhatmini.read_button(screen.displayhatmini.BUTTON_Y):
                pass
            else:
                screen.display_BUTTON_A(temperature, humidity, light_level, 1)


except KeyboardInterrupt:
    print("Shutting down server.")
finally:
    for client in clients:
        client.close()
    server_socket.close()
