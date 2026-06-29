import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from feed.models import Message
from users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.other_username = self.scope["url_route"]["kwargs"]["username"]

        if not self.user.is_authenticated:
            await self.close()
            return

        self.other_user = await sync_to_async(CustomUser.objects.get)(
            username=self.other_username
        )

        # Create a unique room name based on the two user IDs (always sorted so it matches for both)
        user_ids = sorted([self.user.id, self.other_user.id])
        self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_body = data["message"]

        # Save the message to the database asynchronously
        new_msg = await sync_to_async(Message.objects.create)(
            sender=self.user, recipient=self.other_user, body=message_body
        )

        # Broadcast to the Chat Room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_body,
                "sender": self.user.username,
                "time": new_msg.created_at.strftime("%I:%M %p"),
            },
        )

        # Broadcast to the Recipient's Global Notification Network!
        preview = message_body[:40] + "..." if len(message_body) > 40 else message_body
        await self.channel_layer.group_send(
            f"notifications_{self.other_user.id}",
            {
                "type": "send_notification",
                "is_dm": True,
                "actor": self.user.username,
                "message_preview": preview,
            },
        )

    async def chat_message(self, event):
        # Send the broadcasted message to the WebSocket
        await self.send(text_data=json.dumps(event))


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = f"notifications_{self.user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event))
