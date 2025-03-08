import json
import logging

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from timetables.models import Timetable

# Account consumer
class TimetableConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            self.close()
            return

        self.username = user.username
        await self.channel_layer.group_add(
            self.username, 
            self.channel_name
        )
        await self.accept()
        logging.info(f'User connected to room: {self.username}')
        print(f"{self.username} connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.username, 
            self.channel_name
        )
        logging.info(f"User disconnected from room: {self.username}")
        print(f"{self.username} disconnected")

    # Parse the received JSON data
    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Received", json.dumps(data, indent=2))

        operation = data['event']
        

        # Send the message to the group if create_account oppereation
        if operation == 'rename_timetable':
            name = data['sendData']['name']
            batch_id = data['sendData']['batch_id']

            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'rename_timetable',
                    'name': name,
                }
            )
            await self.save_timetable(name, batch_id)
        
       
    # Send the created book to WebSocket
    async def rename_timetable(self, event):
        name = event['name']

        await self.send(text_data=json.dumps({
            'name': name,
        }))


    @sync_to_async
    def save_timetable(self, name, batch_id):
        # user = self.scope.get('user')
        timetables = Timetable.objects.filter(batch_id=batch_id)
        for timetable in timetables:
            timetable.name = name
            timetable.save()

    