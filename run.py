from main import app, db
from service.InitializeService import InitializeService
from app.LSMmain import Main
from service import MqttClient


def initialize():
    print("initializing")
    InitializeService.initialize()
    mqtt = MqttClient.Mqtt(MqttClient._topic)
    main = Main(mqtt)
    main.start()



if __name__ == '__main__':
    initialize()
    app.run(host='0.0.0.0', port=8080)
