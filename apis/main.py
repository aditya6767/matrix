from matrix import MatrixApi
from classify_chat import classify_chat_with_llama


def main():
    try:
        matrix_api = MatrixApi()
        room_ids = matrix_api.get_room_ids()
        
        for room_id in room_ids:
            print(f"Fetching messages from room: {room_id}")
            
            # Step 2: Fetch recent messages in the room
            messages = matrix_api.get_room_messages(room_id)
            print(messages)
            
            classification = classify_chat_with_llama(messages)
            print(f"Classification: {classification}\n")
            print("*"*100)
    except Exception as e:
        print(f"Unable to classify text, {e}")


main()
