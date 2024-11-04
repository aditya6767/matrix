import os
import requests

MATRIX_BASE_URL = os.getenv("MATRIX_BASE_URL", "http://localhost:8008")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "7b309479a0f4bcffad5e0532f60e28ce")


class MatrixApi:
    def __init__(self) -> None:
        self.matrix_base_url = MATRIX_BASE_URL
        self.access_token = ACCESS_TOKEN

    def get_room_ids(self):
        try:
            url = f"{self.matrix_base_url}/_matrix/client/r0/joined_rooms?access_token={self.access_token}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("joined_rooms", [])
        except Exception as e:
            print(f"Unable to fetch rooms, {e}")
            return []

    def get_room_messages(self, room_id, limit=100000):
        try:
            url = f"{self.matrix_base_url}/_matrix/client/r0/rooms/{room_id}/messages?access_token={self.access_token}&limit={limit}&dir=b"
            response = requests.get(url)
            response.raise_for_status()
            messages = response.json().get("chunk", [])
            
            # Filter only text messages
            return "\n".join(
                [msg["content"]["body"] for msg in messages if msg["type"] == "m.room.message" and "body" in msg["content"]]
            )
        except Exception as e:
            print(f"Unable to fetch room messages, {e}")
            return []
