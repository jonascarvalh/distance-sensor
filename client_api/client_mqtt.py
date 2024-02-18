from utils.calibration import Calibration as calib
from paho.mqtt import client as mqtt_client
from decouple import config
from random import randint
import json, requests, os
import pandas as pd
import numpy as np

broker   = config("BROKER")
port     = int(config("PORT"))
topic    = config("TOPIC")
username = config("USER")
password = config("PASS")
URL_API  = config("URL_API")

client_id = f'api-mqtt-{randint(0,100)}'

# Open calibration file
MEASURES_PATH = os.path.join('calibration', 'measures.csv')
df = pd.read_csv(MEASURES_PATH)

measure = np.array(df['measure'])
time    = np.array(df['time'])

# Get least square and create instance calibrator
alpha, p   = calib.minimos_quadrados(time, measure)
calibrator = calib(time, measure, alpha, p)

def calibrate(time):
    dp_erro         = calibrator.dp_erro_ajuste()
    variancia_alpha = calibrator.variancia_alpha(dp_erro)
    desv_alpha      = calibrator.desvio_alpha(variancia_alpha)
    variancia_p     = calibrator.variancia_p(dp_erro)
    desv_p          = calibrator.desvio_p(variancia_p)
    t_student_13    = calibrator.t_student_13graus
    intervalo_conf  = calibrator.intervalo_confianca(t_student_13, dp_erro)
    estimativa_mens = calibrator.estimativa_mensurando(time)
    incerteza_comb  = calibrator.incerteza_combinada(time, intervalo_conf, desv_alpha, desv_p)
    t_student_14    = calibrator.t_student_14graus
    incerteza_exp   = calibrator.incerteza_expandida(incerteza_comb, t_student_14)

    return round(estimativa_mens), round(incerteza_exp, 2)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('[MQTT] Connected to server.')
        else:
            print('[MQTT] Failure to connect.')
    
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker,port)

    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f'[MQTT] Received {msg.payload.decode()} from {msg.topic} topic')

        if msg.payload.decode():
            info_sensor = json.loads(msg.payload.decode())
            measure, uncertainty = calibrate(info_sensor["time"])
            data = {
                "measure": str(measure),
                "time": str(info_sensor["time"]),
                "uncertainty": str(uncertainty),
            }
            data = json.dumps(data)
            print(data)

            headers = {"Content-Type": "application/json"}

            requests.post(
                url=URL_API,
                data=data,
                headers=headers
            )

    client.subscribe(topic)
    client.on_message = on_message

def run_mqtt():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()