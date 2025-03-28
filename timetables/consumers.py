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
        
        elif operation == 'delete_selected_rows':
            ids = data['sendData']['ids']
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'delete_selected_row_data',
                    'ids': ids,
                }
            )
            await self.delete_selected_row(ids)

        elif operation == 'edit_row':
            rowId = data['sendData']['rowId']
            day = data['sendData']['dataSet']['day']
            unit_code = data['sendData']['dataSet']['unit_code']
            unit_name = data['sendData']['dataSet']['unit_name']
            start_time = data['sendData']['dataSet']['start_time']
            end_time = data['sendData']['dataSet']['end_time']
            lecturer = data['sendData']['dataSet']['lecturer']
            campus = data['sendData']['dataSet']['campus']
            mode = data['sendData']['dataSet']['mode']
            room = data['sendData']['dataSet']['room']
            group = data['sendData']['dataSet']['group']
            await self.channel_layer.group_send(
                self.username,
                {
                    'type': 'edit_row_data',
                    'day': day,
                    'rowId': rowId,
                    'end_time': end_time,
                    'unit_code': unit_code,
                    'unit_name': unit_name,
                    'start_time': start_time,
                    'lecturer': lecturer,
                    'campus': campus,
                    'mode': mode,
                    'room': room,
                    'group': group,
                }
            )
            await self.edit_row(rowId, day, end_time, unit_code, unit_name, start_time, lecturer, campus, mode, room, group)
        
       
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

    # Send the deleted selected row to WebSocket
    async def delete_selected_row_data(self, event):
        ids = event['ids']

        await self.send(text_data=json.dumps({
            'ids': ids,
        }))

    # Send the edited row to WebSocket
    async def edit_row_data(self, event):
        rowId = event['rowId']

        await self.send(text_data=json.dumps({
            'rowId': rowId,
        }))

    async def subscription_updated(self, event):
        await self.send(text_data=json.dumps({
            "event": "subscription_updated",
            "message": event["message"],
            "tier": event["tier"],
            "amount": event["amount"],
            "status": event["status"],
        }))



    @sync_to_async
    def save_timetable(self, name, batch_id):
        timetables = Timetable.objects.filter(batch_id=batch_id)
        for timetable in timetables:
            timetable.name = name
            timetable.save()

    @sync_to_async
    def delete_timetable(self, batch_id):
        timetables = Timetable.objects.filter(batch_id=batch_id)
        for timetable in timetables:
            timetable.delete()

    @sync_to_async
    def delete_row(self, rowId):
        timetable = Timetable.objects.get(id=rowId)
        timetable.delete()

    @sync_to_async
    def delete_selected_row(self, ids):
        Timetable.objects.filter(id__in=ids).delete()
        print("Deleted", ids)

    @sync_to_async
    def edit_row(self, rowId, day, end_time, unit_code, unit_name, start_time, lecturer, campus, mode, room, group):
        # user = self.scope.get('user')
        timetable = Timetable.objects.get(id=rowId)
        timetable.day = day
        timetable.end_time = end_time
        timetable.unit_code = unit_code
        timetable.unit_name = unit_name
        timetable.start_time = start_time
        timetable.lecturer = lecturer
        timetable.campus = campus
        timetable.mode_of_study = mode
        timetable.lecture_room = room
        timetable.group = group
        timetable.save()

    