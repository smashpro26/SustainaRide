import time
from gtts import gTTS
import pygame
import threading
import atexit

# Global variable to track the audio thread
audio_thread = None
terminate_audio_thread = False  # Flag to indicate if the thread should terminate

# Function to play audio in a separate thread
def play_audio():
    global terminate_audio_thread
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if terminate_audio_thread:
            pygame.mixer.music.stop()  # Terminate audio playback
            break
        time.sleep(1)

# Function to stop the audio thread gracefully
def stop_audio_thread():
    global audio_thread, terminate_audio_thread
    if audio_thread and audio_thread.is_alive():
        terminate_audio_thread = True  # Set the flag to terminate the thread

# Register the function to stop the audio thread when the program exits
atexit.register(stop_audio_thread)

def play_text_as_audio(text):
    global audio_thread, terminate_audio_thread
    terminate_audio_thread = False  # Reset the termination flag
    tts = gTTS("<speed=2>"+text)
    tts.save("output.mp3")

    # Create a thread to play audio
    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()
