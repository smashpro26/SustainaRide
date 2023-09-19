import pyaudio
import wave
import assemblyai as aai
import os

# Set the audio parameters
FORMAT = pyaudio.paInt16  # Format for audio recording
CHANNELS = 1              # Number of audio channels (1 for mono, 2 for stereo)
RATE = 44100              # Sample rate (samples per second)

# Initialize the audio stream and frames list
audio = pyaudio.PyAudio()
frames = []

# Function to start recording
def start_recording():
    global frames
    frames = []  # Clear the frames list
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=1024)
    print("Recording...")
    return stream

# Function to stop recording and save the audio
def stop_recording(stream, output_filename):
    stream.stop_stream()
    stream.close()
    print("Finished recording.")
    save_audio(output_filename)

# Function to save the recorded audio as a WAV file
def save_audio(output_filename):
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print(f"Audio saved as {output_filename}")

#============================AssemblyAI Speach To Text========================================
aai.settings.api_key = os.environ['ASSEMBLYAI_API_TOKEN']
FILE_URL = "https://github.com/AssemblyAI-Examples/audio-examples/raw/main/20230607_me_canadian_wildfires.mp3"
transcriber = aai.Transcriber()
def transcribe():
    transcript = transcriber.transcribe(FILE_URL)
    return transcript
