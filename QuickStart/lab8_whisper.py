import os,json,openai,pyaudio,wave
from dotenv import load_dotenv
from rich import print as pprint

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_type = "azure"

def record_audio(duration=5, rate=44100, channels=2, chunk=1024):
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=pyaudio.paInt16,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
        
        print("Recording...")
        frames = []
        for i in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)

        print("Finished recording...")
    except Exception as e:
        print(f"Error occurred while setting up the audio stream: {e}")
    finally:
        if 'stream' in locals():
            stream.stop_stream()
            stream.close()
        p.terminate()

    audio_data = b''.join(frames)
    return audio_data

def save_as_wav(audio_data, filename="recorded_audio.wav", rate=48000, channels=2):
    with wave.open(filename,'wb') as wf:
        wf.setnchannels(channels)   
        wf.setsampwidth(2)
        wf.setframerate(rate)
        wf.writeframes(audio_data)
    print(f"Audio saved as '{filename}'")

def list_audio_devices():
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    for i in range(device_count):
        print(p.get_device_info_by_index(i))
    p.terminate()

def recognize_audio_by_whisper(filename):
    with open(filename,"rb") as audio_file:
        result = openai.audio.transcriptions.create(
            model = "whisper",
            file = audio_file
        )

    pprint(result)

def main():
    audio_data = record_audio(duration=5)
    print(f"Audio data length: {len(audio_data)} bytes")

    save_as_wav(audio_data)

    recognize_audio_by_whisper("recorded_audio.wav")

if __name__ == "__main__":
    main()