from time import sleep as delay
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime as dt
from threading import Thread



class AzureClient:

    def __init__(self, connectionString):
        self.connectionString = connectionString
        print(self.connectionString)
        #asyncio.run(self.publishMessage("test"))
        #asyncio.run(self.runAzureMessageSystem)


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



    async def publishMessage(self, msg):

        device_client = IoTHubDeviceClient.create_from_connection_string(self.connectionString)
        print(self.connectionString)
        if not device_client.connected:
            await device_client.connect()
            device_client.on_message_received = self.receiveMessage
        print("Trying to publish...")
        await device_client.send_message(msg)
        print("Message sent!")
        #await device_client.disconnect()



