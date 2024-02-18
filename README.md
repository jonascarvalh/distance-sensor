<div align="center">
    <img alt="hc-sr04" src="https://i.ibb.co/R9LKWXH/sensor-de-movimento.png" width="100"/>
    <h1 style="border-bottom: none;">Distance Sensor</h1>
    <p>Measure and calibrate distance sensor data using and show in a web page.</p>
</div>


## 🎴 Preview
<div align="center">
    <img alt="Dashboard" src="https://i.ibb.co/NKNXYGP/unnamed.png" width="612"/>
</div>

## ✨ Features
- 📏 Measurement and calibration of the HC-SR04 sensor;
- 📶 Communication via MQTT protocol and API;
- 📈 Dashboard made through a web page.

## 🖥️ Systems
- ESP32 Code;
- Client MQTT;
- API;
- Web Page.

## 📚 How it works?
This project aims to collect measurements from the HC-SR04 ultrasonic sensor, send them to an MQTT broker, which in turn will provide the data to the MQTT Client, which is responsible for performing the calibration based on the flight time received. After this, the client will send the calibrated data to an API, which will record the calibrated sensor data in the database. Thus, a web application will consume this API and display the obtained data visually.

Calibration is done using statistical calculations such as linear regression to estimate the measurement and combined and expanded uncertainty to estimate the measurement error.
<div align="center">
    <img alt="Project Architecture" src="https://i.ibb.co/SxNKfw6/arq-sensores-mqtt-1.png" width="512"/>
    <p>Attention: Each folder has a specific functionality related to the project, they also have a readme file.</p>
</div>