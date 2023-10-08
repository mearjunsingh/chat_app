import html
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.aes import AESCipher
from chat.hate_speech import is_hate_speech
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

        _message = "Message Not Sent, Hate Speech Detected"
        _hate_speech = is_hate_speech(message)
        if not _hate_speech:
            # create message object in database
            aes = AESCipher(self.room.key)
            ciphertext = aes.encrypt(message)
            await sync_to_async(Message.objects.create)(
                room=self.room,
                user=self.user,
                message=ciphertext,
            )

            # Parse message
            _message = html.escape(message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "chat_message",
                "message": _message,
                "user": self.user,
                "hate_specch": _hate_speech,
            },
        )

    async def chat_message(self, event):
        # Get parameters from event
        message = event["message"]
        user = event["user"]
        hate_speech = event["hate_specch"]

        # Send message to WebSocket
        data = {"message": message, "user": user, "hate_speech": hate_speech}
        await self.send(text_data=json.dumps(data))
