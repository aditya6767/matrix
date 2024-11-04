import os
import requests
import json

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://0.0.0.0:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")


def classify_chat_with_llama(chat_text):
    # Define the prompt for classification
    prompt = f"""
    Classify the following WhatsApp room as either "family" or "nonfamily" based on the messages exchanged. 

    Definitions:
    - A "family" room generally contains messages about personal updates, family gatherings, and messages directed towards family members.
    - A "nonfamily" room focuses on work, business, or other nonfamily-related topics.

    Examples:

    Messages:
    - "Hey mom, let's plan the dinner for Sunday."
    - "Are you coming over for Thanksgiving this year?"
    - "Please tell dad I'll be there by 6 PM."
    - "How's grandma doing?"

    Classification: family

    ---

    Messages:
    - "Please send me the project files by tomorrow."
    - "Can we reschedule the meeting to next week?"
    - "I'll need the latest report for review."
    - "Check with the finance team about the budget approval."

    Classification: nonfamily

    ---

    Messages:
    - "Don't forget to bring your swimwear for the beach trip, everyone!"
    - "Let's meet at our usual spot for the family reunion."
    - "Happy birthday, uncle! Wish you all the best."
    - "I'll be bringing the dessert for the gathering."

    Classification: family

    ---

    Messages:
    - "The deadline for the project submission is next Friday."
    - "Can someone take over the presentation for me?"
    - "I'll be out of office tomorrow, but reachable on email."
    - "The team meeting is scheduled for 10 AM tomorrow."
    - "bruh"
    - "docker-compose.yml"

    Classification: nonfamily

    ---

    Messages:
    - "Family dinner is this Saturday. See you all there!"
    - "Let's plan our vacation together."
    - "We should get mom a gift for her birthday."
    - "Hey sis, are you coming home this weekend?"

    Classification: family

    ---

    Messages:
    - "Please review the attached document before our meeting."
    - "Forward the email to the client and let them know."
    - "Let's discuss the project timeline tomorrow."
    - "Is the contract ready for review?"
    - "Hello, I'm a WhatsApp bridge bot."

    Classification: nonfamily

    ---

    Now, classify the following room based on the messages below.

    Messages:
    {chat_text}

    Answer with either "family" or "nonfamily" only.
    """
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "temperature": 0.0
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True)
        response.raise_for_status()

        # Accumulate the streamed response
        full_response = ""

        # Read each line as a chunk from the streamed response
        for chunk in response.iter_lines():
            if chunk:
                # Each chunk is a separate JSON string, so parse it
                chunk_data = json.loads(chunk)

                # Append the response part if available
                if "response" in chunk_data:
                    full_response += chunk_data["response"]

                # Check if the response is done
                if chunk_data.get("done", False):
                    break  # Exit loop when the response is complete

        # Strip and process the final response text
        result_text = full_response.strip().lower()
        print("Full response from model:", result_text)  # Debugging line

        # Determine classification based on final response text
        if "family" in result_text and "nonfamily" not in result_text:
            return "family"
        elif "nonfamily" in result_text:
            return "nonfamily"
        else:
            return "uncertain"

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Llama 2 model: {e}")
        return "error"
