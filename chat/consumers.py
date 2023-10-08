import html
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.aes import AESCipher
from chat.models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room = await sync_to_async(Room.objects.get)(
            name=self.room_name,
        )
        self.user = self.scope["url_route"]["kwargs"]["user"]

        # Join room group
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        # read recieved message
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # create message object in database
        aes = AESCipher(self.room.key)
        ciphertext = aes.encrypt(message)
        await sync_to_async(Message.objects.create)(
            room=self.room,
            user=self.user,
            message=ciphertext,
        )

        # Send message to room
        message = html.escape(message)
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": message,
                "user": self.user,
            },
        )

    async def chat_message(self, event):
        # Get parameters from event
        message = event["message"]
        user = event["user"]

        # Send message to WebSocket
        data = {"message": message, "user": user}
        await self.send(text_data=json.dumps(data))
