import assemblyai as aai

aai.settings.api_key = f"7162179352ae4f60a782772e98478ec9"

def on_open(session_opened: aai.RealtimeSessionOpened):
  "This function is called when the connection has been established."

  print("Session ID:", session_opened.session_id)

def on_data(transcript: aai.RealtimeTranscript):
  "This function is called when a new transcript has been received."

  if not transcript.text:
    return

  if isinstance(transcript, aai.RealtimeFinalTranscript):
    print(transcript.text, end="\r\n")
  else:
    print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
  "This function is called when the connection has been closed."

  print("An error occured:", error)

def on_close():
  "This function is called when the connection has been closed."

  print("Closing Session")

  transcriber = aai.RealtimeTranscriber(
  on_data=on_data,
  on_error=on_error,
  sample_rate=44_100,
  on_open=on_open, # optional
  on_close=on_close, # optional
)