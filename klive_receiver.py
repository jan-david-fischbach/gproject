import paho.mqtt.client as mqtt
import json
import requests
import pathlib
import tempfile
import socket
import time

if __name__ == "__main__":
    def on_message(client, userdata, message):
        with tempfile.TemporaryDirectory() as tmpdirname:
            payload = str(message.payload.decode("utf-8"))
            print("message received " , payload)
            print("message topic=",message.topic)
            print("message qos=",message.qos)
            print("message retain flag=",message.retain)
            data = json.loads(payload)
            r = requests.get("http://localhost:8084/gds/")
            filename = pathlib.Path(data["gds"]).name
            fullpath = pathlib.Path(tmpdirname)/filename
            open(fullpath, 'wb').write(r.content)
            data["gds"] = str(fullpath)

            data_string = json.dumps(data)
            try:
                conn = socket.create_connection(("127.0.0.1", 8082), timeout=1.0)
                data_string = data_string + "\n"
                data_string = (
                    data_string.encode() if hasattr(data_string, "encode") else data_string
                )
                print(f"forward with {data_string}")
                conn.sendall(data_string)
                conn.close()
            except OSError:
                print("OSError")
                pass
            time.sleep(10)

    mqtt_client = mqtt.Client("klive receiver")
    mqtt_client.connect("localhost")
    mqtt_client.subscribe("klive")
    mqtt_client.on_message=on_message
    print("connected")
    mqtt_client.loop_forever()


