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
        

        # Send the message to the group if operation is rename_timetable
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

        elif operation == 'delete_timetable':
            batch_id = data['sendData']['batch_id']
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'delete_timetable_data',
                    'batch_id': batch_id,
                }
            )
            await self.delete_timetable(batch_id)
        elif operation == 'delete_row':
            rowId = data['sendData']['rowId']
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'delete_row_data',
                    'rowId': rowId,
                }
            )
            await self.delete_row(rowId)
        
       
    # Send the created book to WebSocket
    async def rename_timetable(self, event):
        name = event['name']

        await self.send(text_data=json.dumps({
            'name': name,
        }))

    # Send the created book to WebSocket
    async def delete_timetable_data(self, event):
        batch_id = event['batch_id']

        await self.send(text_data=json.dumps({
            'batch_id': batch_id,
        }))
    # Send the deleted row to WebSocket
    async def delete_row_data(self, event):
        rowId = event['rowId']

        await self.send(text_data=json.dumps({
            'rowId': rowId,
        }))


    @sync_to_async
    def save_timetable(self, name, batch_id):
        timetables = Timetable.objects.filter(batch_id=batch_id)
        for timetable in timetables:
            timetable.name = name
            timetable.save()

    @sync_to_async
    def delete_timetable(self, batch_id):
        # user = self.scope.get('user')
        timetables = Timetable.objects.filter(batch_id=batch_id)
        for timetable in timetables:
            timetable.delete()

    @sync_to_async
    def delete_row(self, rowId):
        # user = self.scope.get('user')
        timetable = Timetable.objects.get(id=rowId)
        timetable.delete()

    