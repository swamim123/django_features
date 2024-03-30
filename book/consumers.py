# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            if text_data.strip():
                try:
                    data_json = json.loads(text_data)
                    if text_data.strip():
                        if text_data.upper() == "HI":
                            response_message = "Hello"
                        elif text_data.upper() == "HELLO":
                            response_message = "Hello, how are you?"
                        elif 'numbers' in data_json and isinstance(data_json['numbers'], list):
                            numbers = data_json['numbers']
                            response_message = sum(numbers)
                        elif 'req_params' in data_json and isinstance(data_json['req_params'], dict):
                            name = data_json['req_params']['name']
                            qty = data_json['req_params']['qty']
                            amount = data_json['req_params']['amount']
                            response_message = f'{name} orderd disel of quantity {qty} ltr and amount cost Rs.{amount}'
                        else:
                            response_message = "Sorry, I didn't understand that."

                        await self.send(text_data=json.dumps({
                            'message': response_message
                        }))
                    else:
                        print("Received empty data.")

                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", str(e))
            else:
                if text_data.upper() == "HI":
                    response_message = "Hello"
                    await self.send(text_data=json.dumps({
                        'message': response_message
                    }))
                else:
                    print("Received empty data or unknown message:", text_data)
        except Exception as e:
            print("Error processing data:", str(e))
