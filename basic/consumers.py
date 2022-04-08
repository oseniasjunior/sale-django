from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print('conectou')
        await self.accept()
        await self.channel_layer.group_add('chat', self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard('chat', self.channel_name)

    async def group_message(self, event):
        await self.send_json(content=event['content'])

    async def receive_json(self, event, **kwargs):
        await self.channel_layer.group_send('chat', {
            'type': 'group.message',
            'content': event
        })
