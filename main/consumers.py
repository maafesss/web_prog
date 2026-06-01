import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
import os

logger = logging.getLogger(__name__)

class LikeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            redis_url = os.environ.get('REDIS_URL')
            if not redis_url:
                logger.error("REDIS_URL environment variable not set")
                await self.close()
                return

            self.channel_layer = get_channel_layer()
            await self.channel_layer.group_add("likes_group", self.channel_name)
            await self.accept()
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            if hasattr(self, 'channel_layer') and self.channel_layer:
                await self.channel_layer.group_discard(
                    "likes_group",
                    self.channel_name
                )
        except Exception as e:
            logger.error(f"Disconnection error: {str(e)}")

    async def like_update(self, event):
        try:
            await self.send(text_data=json.dumps({
                'car_id': event['car_id'],
                'likes_count': event['likes_count'],
                'user_has_liked': event['user_has_liked']
            }))
        except Exception as e:
            logger.error(f"Error sending update: {str(e)}")