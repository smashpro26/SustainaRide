import pvrecorder
import wave
import os
import assemblyai as aai
import wave
import struct
import threading

recorder = pvrecorder.PvRecorder(device_index=-1, frame_length=512)
recording = False
audio = []

# Function to start recording
def start_recording():
    global recording
    global audio
    global recorder
    recording = True
    recorder.start()
    record_thread = threading.Thread(target=record)
    record_thread.start()
    print("Recording...")

def record():
     while recording:
            print("got in here")
            frame = recorder.read()
            audio.extend(frame)
# Function to stop recording and save the audio
def stop_recording(output_filename):
    global recording
    recording = False
    recorder.stop()
    save_audio(audio, output_filename)

# Function to save the recorded audio as a WAV file


# Function to save the recorded audio as a WAV file
def save_audio(audio_frames, output_filename):
    with wave.open(output_filename, 'wb') as f:
        f.setparams((1, 2, 16000, 0, "NONE", "NONE"))  # Adjust parameters as needed
        f.writeframes(struct.pack("h" * len(audio_frames), *audio_frames))
    print(f"Audio saved as {output_filename}")



#============================AssemblyAI Speech To Text========================================
aai.settings.api_key = os.environ['ASSEMBLYAI_API_TOKEN']

#transcribing the audio
def transcribe_audio(file_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)
    print (transcript.text)
    return transcript


