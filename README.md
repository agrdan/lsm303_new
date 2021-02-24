# lsm303
The project is under development and it's just a fast prototype for testing, code and general usage will be improved before the first release.

LSM303 project is made for Raspberry Pi (some of the requirements can be installed only on devices that have/use I2C protocol)
Project is made for checking window state, if the window is open, closed, half-open, etc, and the project is part of air quality project along with BME680 sensor.
For the project, you will need LSM303c magnetometer, any raspberry pi, and some sort of ferromagnetic part that will make distortions on your magnetic field.

Before using, for better results, a magnetometer needs to be calibrated (with hard iron calibration)
After calibration, it needs to setup referent points of the window state.
The project is not generic, and needs a lot of changes if you need it for other use cases.
The project is using Azure IoT Hub for publishing messages, but also have prepared paho-MQTT client
which can be used free over my broker: iot-smart-systems.eu; port: 1883

TODO: before release v1.0, I will provide as many as possible generic use cases and simplified use in general
Wiring and video of project demo will be provided after v1.0 release.
