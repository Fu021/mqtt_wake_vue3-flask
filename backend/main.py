from mqtt_client import MqttClient
from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import threading
import sqlite3

CHECK_ALIVE = 0
ALIVE = 1
WAKE = 2

app = Flask(__name__)
CORS(app)

class Backend:
    def __init__(self):
        self.device_info = []
        self.update_from_db()

        self.client = MqttClient(self.process_callback)
        self.alive_thread = threading.Thread(target=self.check_alive)
        self.alive_thread.start()

    def update_from_db(self):
        self.device_info = []
        db = sqlite3.connect('devices.db')
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        db.commit()

        cursor.execute("SELECT * FROM devices")
        rows = cursor.fetchall()
        for row in rows:
            self.device_info.append({'id':row[0],'name':row[1],'alive':0,'last_response_time':0})

        db.close()

    def delete_db(self,id):
        db = sqlite3.connect('devices.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM devices WHERE id = ?", (id,))
        row = cursor.fetchone()

        if row is None:
            db.close()
            return -1
        else:
            cursor.execute("DELETE FROM devices WHERE id = ?", (id,))
            db.commit()
            db.close()
            self.update_from_db()
            return 1
        
    def add_db(self,msg):
        id = msg['id']
        name = msg['name']

        if type(id) != int or id < 0 or type(name) != str or name == '':
            return -1

        db = sqlite3.connect('devices.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM devices WHERE id = ?", (id,))
        row = cursor.fetchone()

        if row is not None:
            db.close()
            return -2
        else:
            cursor.execute("INSERT INTO devices (id, name) VALUES (?, ?)", (id, name))
            db.commit()
            db.close()
            self.update_from_db()
            return 1

    def check_alive(self):
        while True:
            # 设备已经30s没有回应了
            for i in range(len(self.device_info)):
                if time.time() - self.device_info[i]['last_response_time'] > 30:
                    self.device_info[i]['alive'] = 0

            if self.client.connected:
                for i in range(len(self.device_info)):
                    self.client.send({'id': self.device_info[i]['id'], 'msg': CHECK_ALIVE, 'time': time.time()})
                time.sleep(5)

    def process_callback(self,msg):
        try:
            if msg['time']-time.time() < 300 and msg['msg'] == ALIVE:
                for i in self.device_info:
                    if i['id'] == msg['id']:
                        i['alive'] = 1
                        i['last_response_time'] = time.time()
                        break
        except:
            print(f"无法解析的消息:{msg}")

    def wake(self,id):
        self.client.send({'id': id, 'msg': WAKE, 'time': time.time()})

backend = Backend()

@app.route('/api/connect', methods=['GET'])
def check_connect():
    return jsonify({'msg': backend.client.connected})
    
@app.route('/api/check_alive', methods=['POST'])
def alive_send():
    msg = request.get_json()
    for i in backend.device_info:
        if i['id'] == msg['id']:
            return jsonify({'msg':i['alive']})
    return jsonify({'msg':-1})

@app.route('/api/wake', methods=['POST'])
def wake():
    msg = request.get_json()
    backend.wake(msg['id'])
    return ""

@app.route('/api/get_info', methods=['GET'])
def send_device_info():
    return jsonify(backend.device_info)

@app.route('/api/delete', methods=['POST'])
def delete_device():
    msg = request.get_json()
    res = backend.delete_db(msg['id'])
    return jsonify({'msg':res})

@app.route('/api/add',methods=['POST'])
def add_device():
    msg = request.get_json()
    res = backend.add_db(msg)
    return jsonify({'msg':res})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5005',debug=False)