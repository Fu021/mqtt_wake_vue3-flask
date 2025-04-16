import paho.mqtt.client as mqtt
import json
import time

class MqttClient:
    def __init__(self, process_callback):
        self.username = ''
        self.password = ''
        self.topic = 'wake'
        self.url = ''
        self.port = 8883
        self.process_callback = process_callback
        self.connected = False

        self.client = mqtt.Client(client_id="")
        self.client.username_pw_set(self.username,self.password)
        self.client.tls_set()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        self.client.connect(self.url,self.port)
        self.client.loop_start()

    def on_connect(self,client:mqtt.Client,userdata,flags,rc):
        self.connected = True
        client.subscribe(self.topic)

    def on_message(self,client:mqtt.Client,userdata,msg:mqtt.MQTTMessage):
        msg = msg.payload.decode()
        try:
            msg = json.loads(msg)
        except:
            pass
        self.process_callback(msg)

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        while not self.connected:
            try:
                self.client.reconnect()
                self.connected = True
            except:
                time.sleep(3)
        
    def send(self,msg:dict):
        if self.connected:
            data = json.dumps(msg)
            self.client.publish(self.topic,data)
            return 1
        else:
            return 0