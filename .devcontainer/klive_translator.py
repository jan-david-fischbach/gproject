import paho.mqtt.client as mqtt

import socketserver
import json
from flask import Flask, request
import tempfile
import shutil
import multiprocessing

with tempfile.TemporaryDirectory() as tmpdirname:
    filename = "tmp.gds"
    app = Flask(__name__, static_folder=tmpdirname)

    @app.route('/gds/')
    def root():
        print(f"hello looking for file in {tmpdirname}")
        return app.send_static_file(f"{filename}")

    class MyTCPHandler(socketserver.BaseRequestHandler):
        """
        The request handler class for our server.

        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.
        """

        def handle(self):
            # self.request is the TCP socket connected to the client
            raw_data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            data = json.loads(raw_data)
            print(data)
            if "gds" in data: 
                shutil.copy(data["gds"], f"{tmpdirname}/{filename}") 

            mqtt_client = mqtt.Client("klive_translator")
            mqtt_client.connect("localhost")
            mqtt_client.publish("klive", raw_data) 
            mqtt_client.disconnect()
    
    def start_fileserver():
        app.run(host='0.0.0.0', port=8084)

    def start_mqtt_translator():
        HOST, PORT = "localhost", 8082

        # Create the server, binding to localhost on port 9999
        with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
            # Activate the server; this will keep running until you
            # interrupt the program with Ctrl-C
            server.serve_forever()

    if __name__ == "__main__":

        p = multiprocessing.Process(target=start_fileserver)
        p.start()

        start_mqtt_translator()