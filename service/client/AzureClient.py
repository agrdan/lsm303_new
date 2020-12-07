from time import sleep as delay
import asyncio
from azure.iot.device import IoTHubDeviceClient
from datetime import datetime as dt



class AzureClient:

    def __init__(self, connectionString):
        self.connectionString = connectionString

        asyncio.run(self.runAzureMessageSystem)


    async def publish(self, msg):
        await self.deviceClient.send_message(msg)


    def receiveMessage(self, message):
        print("Message received [{}]".format(dt.now()))
        print(message.data)
        print(message.custom_properties)


    async def runAzureMessageSystem(self):
        self.deviceClient = IoTHubDeviceClient.create_from_connection_string(self.connectionString)
        await self.deviceClient.connect()
        self.deviceClient.on_message_received = self.receiveMessage