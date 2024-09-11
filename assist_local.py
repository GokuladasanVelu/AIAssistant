from openai import OpenAI
import ollama
import time
from pygame import mixer
import os

# Initialize the OpenAI client and mixer
client = OpenAI()
mixer.init()

# Global variable to store conversation history
conversation_history = []

def ask_question_memory(question):
    try:
        system_message = """You are Jarvis, the AI assistant from Iron Man. Remember, I am not Tony Stark, just your commander. You are formal and helpful, and you don't make up facts, you only comply to the user requests.
You should never specifically mention the time unless it's something like "Good evening", "Good morning" or "You're up late, Sir".
Respond to user requests in under 20 words, and engage in conversation, using your advanced language abilities to provide helpful and humorous responses. Call the user by 'Sir'"""

        # Add the new question to the conversation history
        conversation_history.append({'role': 'user', 'content': question})
        
        # Include the system message and conversation history in the request
        response = ollama.chat(model='llama3.1', messages=[
            {'role': 'system', 'content': system_message},
            *conversation_history
        ])
        
        # Add the AI response to the conversation history
        conversation_history.append({'role': 'assistant', 'content': response['message']['content']})
        
        return response['message']['content']
    except ollama.ResponseError as e:
        print(f"An error occurred: {e}")
        return f"The request failed: {e}"

def generate_tts(sentence, speech_file_path):
    response = client.audio.speech.create(model="tts-1", voice="echo", input=sentence)
    response.stream_to_file(speech_file_path)
    return str(speech_file_path)

def play_sound(file_path):
    mixer.music.load(file_path)
    mixer.music.play()

def TTS(text):
    speech_file_path = generate_tts(text, "speech.mp3")
    play_sound(speech_file_path)
    while mixer.music.get_busy():
        time.sleep(1)
    mixer.music.unload()
    os.remove(speech_file_path)
    return "done"